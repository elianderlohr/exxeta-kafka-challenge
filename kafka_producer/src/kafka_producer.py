from confluent_kafka import Producer
import json
import time
import logging
import random
import csv
import os
import sys

from libs.helper import load_schema, check_schema, encode_failed


from dotenv import load_dotenv


class KafkaProducer:
    # producer
    producer: Producer = None

    def __init__(self, dotenv_path=".env"):
        # Load environment variables
        load_dotenv(override=False, dotenv_path=dotenv_path)

        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        logging.basicConfig(
            format="%(asctime)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=os.getenv("LOG_FILE_PATH"),
            filemode="w",
        )

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def create_producer(self):
        """
        create_producer Creates a Kafka Producer

        :return: The Kafka Producer
        """
        print("Trying to setup Kafka Producer...")
        self.producer = Producer(
            {"bootstrap.servers": str(os.getenv("KAFKA_BOOTSTRAP_SERVERS"))}
        )
        print("Kafka Producer has been initiated...")

    def receipt(self, err, msg):
        """
        receipt Callback function for message produce

        :param err: The error message
        :param msg: The message
        """
        if err is not None:
            self.logger.error("Error: {}".format(err))
            m = json.dumps(msg.value().decode("utf-8"))

            # extract wiki name from msg.topic
            wiki = msg.topic().split("-")[1]

            self.produce_message(
                "wikipedia-{}-failed-dlq".format(wiki), encode_failed(m)
            )
        else:
            # parse string to json object
            m = json.loads(msg.value().decode("utf-8"))

            message = "Produced message on topic {} with wikipedia change id {}".format(
                msg.topic(), m["id"]
            )
            self.logger.info(message + "\n")
            print(message)

    def produce_message(self, topic: str, message):
        """
        produce_message Produces a message to a topic

        :param topic: The topic to produce to
        :param message: The message to produce
        """

        try:
            # Produce the message
            self.producer.produce(topic, message.encode("utf-8"), callback=self.receipt)
            self.logger.info(
                "Message {} produced to topic {}".format(message.encode("utf-8"), topic)
            )

            # Flush the producer > wait for all messages to be delivered
            self.producer.flush()
            self.logger.info("Producer flushed")

        except Exception as e:
            self.logger.error("Failed to produce message: {}".format(e))

    def produce_csv_messages(self, path, encoding="utf-8", delimiter=","):
        """
        produce_csv_messages Reads the data from the csv file

        :param path: The path to the csv file
        :param encoding: The encoding of the csv file (default: utf-8)
        :param delimiter: The delimiter of the csv file (default: ,)
        """

        # load schema from src\static\wikipedia-schema.json
        schema = load_schema(
            os.path.join(
                self.ROOT_DIR,
                "static/wikipedia-schema.json",
            )
        )

        with open(path, encoding=encoding) as csvfile:
            # read csv file
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                # check if row is valid json and valid schema
                if check_schema(row, schema):
                    # produce message to topic wikipedia-changes-success
                    self.produce_message("wikipedia-success", json.dumps(row))

                    # produce message to topic wikipedia-WIKI-success
                    self.produce_message(
                        "wikipedia-{}-success".format(row["wiki"]),
                        json.dumps(row),
                    )
                else:
                    self.produce_message(
                        "wikipedia-failed-schema",
                        encode_failed(row),
                    )

                # Generate a random sleep time between 0 and 1 seconds
                sleep = random.random()
                # Sleep for the random time
                time.sleep(sleep)

                print("Sleeping for {} seconds".format(sleep))
        
        
        print()
        print("Finished producing messages. Shutting down producer...")

    def run(self):
        """
        run Sets up the producer
        """
        # Create the producer
        self.create_producer()

        # Path to the csv file
        data_path = os.path.join(
            self.ROOT_DIR,
            "../data/raw/de_challenge_sample_data.csv",
        )
        # Parse the csv file and produce the messages
        self.produce_csv_messages(data_path)


if __name__ == "__main__":
    landing_zone = KafkaProducer()
    try:
        landing_zone.run()
    except KeyboardInterrupt:
        landing_zone.logger.info("%% Aborted by user")
    except Exception as e:
        landing_zone.logger.error(e)
