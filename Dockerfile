# Use an official Python runtime as an image
FROM python:3.10.7-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Flask apps listen to port 5000
EXPOSE 5000

# Install the project
COPY /src/ /src/

# Copy app code
COPY /services/app/ /src/app/

# Install app service dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r /src/app/requirements.txt

COPY /setup.py /
RUN pip3 install -e .

# Launch Flask App
CMD python /src/app/app.py