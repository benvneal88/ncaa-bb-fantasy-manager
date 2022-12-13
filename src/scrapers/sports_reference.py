import os
import sys
import pandas
from bs4 import BeautifulSoup


sys.path.append(os.getcwd())
from src.utils import data_source as data_src_util
from src.utils import logger as log_util
from src.utils import database as db_util

LOGGER_NAME = 'sports_reference'
LOG_LEVEL = 'INFO'

DATABASE_NAME = 'sportsref'



def get_school_list_raw(is_refresh=False):
    table_name = 'school_list'
    logger = log_util.get_logger(LOGGER_NAME, LOG_LEVEL)
    url = 'https://www.sports-reference.com/cbb/schools/'
    file_path = os.path.join(os.getcwd(), "src", "data", DATABASE_NAME, table_name, "raw", "schools.html")

    if is_refresh:
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            logger.debug(f"\tcreating folder path {dir_path}")
            os.makedirs(dir_path)

        data_src_util.download_file(url, file_path)

    with open(file_path, 'r') as file:
        file_data = file.read()

    return file_data


def transform_school_list_raw(data_str):
    logger = log_util.get_logger(LOGGER_NAME, LOG_LEVEL)
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


def load_schools():
    raw_data = get_school_list_raw(is_refresh=False)
    schools_df = transform_school_list_raw(raw_data)
    engine = db_util.get_engine('fantasy_mgr')
    schools_df.to_sql('tbl_schools', con=engine, if_exists='replace')


if __name__ == '__main__':
    load_schools()