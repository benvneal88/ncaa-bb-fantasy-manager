import os
import pandas
import re
from bs4 import BeautifulSoup
#sys.path.append(os.getcwd())
from api.utils import logger as log_util
from api import model
from api.utils import ingest

LOGGER_NAME = 'sports_reference'
LOG_LEVEL = 'INFO'
ROOT_URL = 'https://www.sports-reference.com'
YEAR = '2023'

DATA_SOURCE = 'sportsref'

ROOT_DATA_PATH = os.path.join(os.getcwd(), "api", "data", DATA_SOURCE)

logger = log_util.get_logger(LOGGER_NAME, LOG_LEVEL)


#####################
## Helper Functions
#####################
def get_roster_url(school):
    engine = model.get_engine()
    query = f"select CONCAT('{ROOT_URL}', url, '{YEAR}.html') as url from {model.STG_SCHOOLS_TABLE_NAME} where School = '{school}'"
    #print(query)
    df = pandas.read_sql_query(query, con=engine)

    if len(df) == 0:
        return None

    return df.loc[0]['url']


######################
## Ingest Functions ##
######################
def get_school_roster_raw(engine, school: str, is_refresh: bool):
    """Fetches roster for school from data source

    engine (SQLAlchemy): the database connection
    school (str) : the name of the school to fetch
    is_refresh (bool) : fetch from web even if data is available locally
    """
    message = f"Fetching roster for school {school}"
    logger.info(message)
    model.write_to_console_logs(engine=engine, message=message)
    object_type = 'rosters'
    school_file_name = school.lower().replace(" ", "")
    file_path = os.path.join(ROOT_DATA_PATH, object_type, "raw", f"{school_file_name}.html")

    # download the object to raw (local) if it doesn't exist
    if not os.path.exists(file_path):
        logger.info(f"Raw local file does not exist. Downloading file...")
        is_refresh = True

    # download file if needed
    if is_refresh:
        url = get_roster_url(school)
        if url is None:
            logger.error(f"No roster url found for school {school}")
        else:
            ingest.download_file(url, file_path)

    with open(file_path, 'r') as file:
        file_data = file.read()

    return file_data


def get_school_list_raw(is_refresh=False):
    """"""
    object_type = 'school_list'
    url = f'{ROOT_URL}/cbb/schools/'
    file_path = os.path.join(ROOT_DATA_PATH, object_type, "raw", "schools.html")

    # download file if needed
    if is_refresh:
        ingest.download_file(url, file_path)

    with open(file_path, 'r') as file:
        file_data = file.read()

    return file_data


#####################
## Transform Functions
#####################
def transform_school_list_raw(data_str):
    soup = BeautifulSoup(data_str, 'html.parser')
    school_html = soup.find(id="schools")

    dfs = pandas.read_html(str(school_html), flavor="bs4")
    schools_df = dfs[0]

    # iterate over schools table and grab the links for the school name
    link_dict = {}
    table = school_html.find("tbody")
    for tr in table.findAll("tr"):
        tds = tr.findAll("td")
        for item in tds:
            try:
                link = item.find('a')['href']
                school_name = item.find('a').text.strip()
                link_dict[school_name] = link
            except:
                pass

    schools_df["url"] = schools_df["School"].map(link_dict)
    #print(schools_df)
    schools_df = schools_df[schools_df.School != 'School']

    return schools_df


def transform_roster_raw(data_str, school_name):
    summary_parse_regex = re.compile(r"([0-9\.]{3,}).*([0-9\.]{3,}).*([0-9\.]{3,}).*")
    name_parse_regex = re.compile(r"([a-zA-Z'\.]+) ([a-zA-Z'\. ]+)")

    def _parse_summary(summary_str):
        groups = re.match(summary_parse_regex, summary_str)
        ppg = groups.group(1)
        rpg = groups.group(2)
        apg = groups.group(3)
        return ppg, rpg, apg

    def _parse_name(name_str):
        groups = re.match(name_parse_regex, name_str)
        try:
            first_name = groups.group(1)
            last_name = groups.group(2)
        except Exception as e:
            logger.error(f"Unable to parse first and last name from {name_str}")
            first_name = 'error'
            last_name = 'error'

        return first_name, last_name

    soup = BeautifulSoup(data_str, 'html.parser')
    roster_html = soup.find(id="roster")
    dfs = pandas.read_html(str(roster_html), flavor="bs4")
    roster_df = dfs[0]
    roster_df["School"] = school_name
    roster_df["PPG"], roster_df["RPG"], roster_df["APG"] = zip(*roster_df['Summary'].apply(lambda x: _parse_summary(x)))
    roster_df = roster_df.drop("Summary", axis=1)

    roster_df["First Name"], roster_df["Last Name"] = zip(*roster_df['Player'].apply(lambda x: _parse_name(x)))
    roster_df = roster_df.drop("Player", axis=1)

    return roster_df


#####################
## Insert Functions
#####################
def insert_stg_schools(engine):
    file_data = get_school_list_raw(is_refresh=False)
    schools_df = transform_school_list_raw(file_data)
    schools_df.to_sql(model.STG_SCHOOLS_TABLE_NAME, con=engine, if_exists='replace')


def insert_stg_roster(engine, school_list=[]):
    logger.info(f"Refreshing rosters from schools: {school_list}")
    model.delete_table(engine, model.STG_ROSTER_TABLE_NAME)

    for school_name in school_list:
        file_data = get_school_roster_raw(engine, school_name, is_refresh=False)
        roster_df = transform_roster_raw(file_data, school_name)
        logger.info(f"Inserting roster {school_name} into table {model.STG_ROSTER_TABLE_NAME}")
        roster_df.to_sql(model.STG_ROSTER_TABLE_NAME, con=engine, if_exists='append')

#
# if __name__ == '__main__':
#     engine = model.get_engine()
#     #insert_stg_schools(engine)
#     school_list = ['Duke', 'North Carolina']
#     insert_stg_roster(engine, school_list)

