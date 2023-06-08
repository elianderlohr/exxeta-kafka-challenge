from confluent_kafka import Producer
import json
import time
import logging
import random
import csv
import os
from libs import helper
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=False)

# global variables
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=os.getenv("LOG_FILE_PATH"),
    filemode="w",
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

print("Trying to setup Kafka Producer...")

p = Producer({"bootstrap.servers": str(os.getenv("KAFKA_BOOTSTRAP_SERVERS"))})


print("Kafka Producer has been initiated...")


def receipt(err, msg):
    """
    receipt Callback function for message produce

    :param err: The error message
    :param msg: The message
    """
    if err is not None:
        logger.error("Error: {}".format(err))
        m = json.dumps(msg.value().decode("utf-8"))

        # extract wiki name from msg.topic
        wiki = msg.topic().split("-")[1]

        produce_message("wikipedia-{}-failed-dlq".format(wiki), helper.encode_failed(m))
    else:
        # parse string to json object
        m = json.loads(msg.value().decode("utf-8"))

        message = "Produced message on topic {} with wikipedia change id {}".format(
            msg.topic(), m["id"]
        )
        logger.info(message + "\n")
        print(message)


def produce_message(topic, message):
    """
    produce_message Produces a message to a topic

    :param topic: The topic to produce to
    :param message: The message to produce
    """
    p.poll(1)

    # Produce the message
    p.produce(topic, message.encode("utf-8"), callback=receipt)
    logger.info(
        "Message {} produced to topic {}".format(message.encode("utf-8"), topic)
    )

    p.flush()


def parse_file(path, encoding="utf-8", delimiter=","):
    """
    parse_file Reads the data from the csv file

    :param path: The path to the csv file
    :param encoding: The encoding of the csv file (default: utf-8)
    :param delimiter: The delimiter of the csv file (default: ,)
    """

    # load schema from src\static\wikipedia-schema.json
    schema = helper.load_schema(
        os.path.join(
            ROOT_DIR,
            "static/wikipedia-schema.json",
        )
    )

    with open(path, encoding=encoding) as csvfile:
        # read csv file
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            # check if row is valid json and valid schema
            if helper.check_schema(row, schema):
                # produce message to topic wikipedia-changes-success
                produce_message("wikipedia-success", json.dumps(row))

                # produce message to topic wikipedia-WIKI-success
                produce_message(
                    "wikipedia-{}-success".format(row["wiki"]),
                    json.dumps(row),
                )
            else:
                produce_message(
                    "wikipedia-failed-schema",
                    helper.encode_failed(row),
                )

            # Generate a random sleep time between 0 and 1 seconds
            sleep = random.random()
            # Sleep for the random time
            time.sleep(sleep)

            print("Sleeping for {} seconds".format(sleep))


if __name__ == "__main__":
    try:
        # Path to the csv file
        data_path = os.path.join(
            ROOT_DIR,
            "../data/raw/de_challenge_sample_data.csv",
        )
        # Parse the csv file and produce the messages
        parse_file(data_path)
    except KeyboardInterrupt:
        logger.info("%% Aborted by user")
    except Exception as e:
        logger.error(e)
