FROM python:3.7.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY src/ src/
#RUN ["chmod", "+x", "/src/init.sh"]

WORKDIR /src

RUN pip install --upgrade pip
RUN pip install -U pip && pip install -r requirements.txt
#RUN pip install -e

RUN useradd app_runner

# allow service user to rwd into the data sufolder
RUN chown -R app_runner:app_runner /src/api/data
RUN chmod -R u=rwx,go=r /src/api/data

USER app_runner

EXPOSE 8080