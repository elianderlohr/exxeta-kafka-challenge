FROM python:3.11.1

RUN apt-get update

COPY kafka_producer/requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN pip install -r requirements.txt

COPY kafka_producer/ /opt/app

# Set environment variables
ENV LOG_FILE_PATH=../../var/log/kafka_producer.log
ENV BASE_FILE_PATH=opt/app/

# kafka
ENV KAFKA_BOOTSTRAP_SERVERS=broker:29092

WORKDIR /

# use unbuffered output
CMD ["python", "-u", "opt/app/src/kafka_producer.py"]