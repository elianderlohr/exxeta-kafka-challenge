FROM python:3.11.1

RUN apt-get update

COPY structured/requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN pip install -r requirements.txt

COPY structured/ /opt/app

# Set environment variables
ENV LOG_FILE_PATH=../../var/log/structured.log
ENV AGGREGATION_FILE_PATH=opt/app/output/aggregation.csv

# kafka
ENV KAFKA_BOOTSTRAP_SERVERS=broker:29092

WORKDIR /

# use unbuffered output
CMD ["python", "-u", "opt/app/src/structured.py"]