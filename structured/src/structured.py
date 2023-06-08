from confluent_kafka import Consumer
import time
import logging
import csv
import os
from dotenv import load_dotenv

# Load environment variables, ensure NO override of system variables
load_dotenv(override=False)

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=os.getenv("LOG_FILE_PATH"),
    filemode="w",
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# global variables
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

print("Trying to setup Kafka Consumer...")

c = Consumer(
    {
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        "group.id": "structured-consumer",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": "true",
    }
)

print("Kafka Consumer has been initiated...")

# Define the topics
topic = "wikipedia-success"
german_topic = "wikipedia-dewiki-success"


# Subscribe to the topic "wikipedia-edits-success"
c.subscribe([topic, german_topic])


def write_aggregations_to_file(global_edits_per_minute, german_edits_per_minute):
    """
    write_aggregations_to_file Writes aggregations to file

    :param global_edits_per_minute: The global edits per minute
    :param german_edits: The german edits per minute
    """

    # check if file exists
    try:
        with open(str(os.getenv("AGGREGATION_FILE_PATH")), "r") as file:
            pass
    except FileNotFoundError:
        # create file and add csv header
        with open(str(os.getenv("AGGREGATION_FILE_PATH")), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["timestamp", "global_edits_per_minute", "german_edits_per_minute"]
            )

    # Write aggregations to csv file
    with open(str(os.getenv("AGGREGATION_FILE_PATH")), "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                global_edits_per_minute,
                german_edits_per_minute,
            ]
        )


def main():
    # Aggregation variables
    global_edits = 0
    german_edits = 0
    start_time = time.time()

    try:
        # Consume messages
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error("Error: {}".format(msg.error()))
                continue

            logger.info("Message received: {}".format(msg.value().decode("utf-8")))

            # Increment global edits count
            if msg.topic() == topic:
                global_edits += 1

            # Check if msg is from German Wikipedia
            if msg.topic() == german_topic:
                german_edits += 1

            # Calculate elapsed time in minutes
            elapsed_minutes = (time.time() - start_time) / 60

            # Perform aggregation per minute
            if elapsed_minutes >= 1:
                global_edits_per_minute = global_edits / elapsed_minutes
                german_edits_per_minute = german_edits / elapsed_minutes

                # Print and save the results
                logger.info(f"Global edits per minute: {global_edits_per_minute}")
                logger.info(f"German edits per minute: {german_edits_per_minute}")

                print(f"Global edits per minute: {global_edits_per_minute}")
                print(f"German edits per minute: {german_edits_per_minute}")

                write_aggregations_to_file(
                    global_edits_per_minute, german_edits_per_minute
                )

                # Reset counters and start time
                global_edits = 0
                german_edits = 0
                start_time = time.time()

    except KeyboardInterrupt:
        logger.info("%% Aborted by user\n")

    finally:
        c.close()


if __name__ == "__main__":
    main()
