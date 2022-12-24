# Use an official Python runtime as an image
FROM python:3.10

# Flask apps listen to port 5000
EXPOSE 5000

# Copy the project code
WORKDIR /ncaa_fantasy/
COPY /ncaa_fantasy/ ./ncaa_fantasy/

# Install the project
COPY setup.py /ncaa_fantasy/setup.py
RUN pip install -e .

# Copy app service code
WORKDIR /ncaa_fantasy/app/
COPY /services/app/ ./

# Install app service dependencies
RUN pip install -r requirements.txt

# Launch Flask App
CMD python /ncaa_fantasy/app/app.py