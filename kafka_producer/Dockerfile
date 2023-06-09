FROM python:3.11.1

RUN apt-get update

COPY landing/requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN pip install -r requirements.txt

COPY landing/ /opt/app

# Set environment variables
ENV LOG_FILE_PATH=../../var/log/landing.log
ENV BASE_FILE_PATH=opt/app/

# kafka
ENV KAFKA_BOOTSTRAP_SERVERS=broker:29092

WORKDIR /

# use unbuffered output
CMD ["python", "-u", "opt/app/src/landing.py"]