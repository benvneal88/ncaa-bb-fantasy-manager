FROM python:3.7.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY src/ src/
WORKDIR /src

RUN pip install --upgrade pip
RUN pip install -U pip && pip install -r requirements.txt
#RUN pip install -e

RUN useradd app_runner
USER app_runner

EXPOSE 8080
ENTRYPOINT ["python3", "init_db.py"]
