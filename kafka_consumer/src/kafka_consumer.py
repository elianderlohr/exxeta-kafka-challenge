from confluent_kafka import Consumer
import time
import logging
import csv
import os
from dotenv import load_dotenv
import sys

# Load environment variables, ensure NO override of system variables
load_dotenv(override=False)

class KafkaConsumer:
    # global vars
    german_edits = 0
    global_edits = 0

    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        logging.basicConfig(
            format="%(asctime)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=os.getenv("LOG_FILE_PATH"),
            filemode="w",
        )

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        
        # Setup Kafka Consumer
        print("Trying to setup Kafka Consumer...")
        self.consumer = Consumer(
            {
                "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                "group.id": "structured-consumer",
                "auto.offset.reset": "earliest",
                "enable.auto.commit": "true",
            }
        )
        print("Kafka Consumer has been initiated...")

        # Define the topics
        self.topic = "wikipedia-success"
        self.german_topic = "wikipedia-dewiki-success"

    def write_aggregations_to_file(
        self, global_edits_per_minute, german_edits_per_minute
    ):
        """
        Writes aggregations to a file

        :param global_edits_per_minute: The global edits per minute
        :param german_edits_per_minute: The German edits per minute
        """

        # Check if the file exists
        file_path = str(os.getenv("AGGREGATION_FILE_PATH"))
        file_exists = os.path.isfile(file_path)

        # Create the file and add CSV header if it doesn't exist
        if not file_exists:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["timestamp", "global_edits_per_minute", "german_edits_per_minute"]
                )

        # Write aggregations to the CSV file
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    global_edits_per_minute,
                    german_edits_per_minute,
                ]
            )

    def process_message(self, message):
        """
        Processes a Kafka message

        :param message: The Kafka message
        """
        topic = message.topic()
        value = message.value().decode("utf-8")

        self.logger.info("Message received: {}".format(value))

        # Increment global edits count
        if topic == self.topic:
            self.global_edits += 1

        # Check if the message is from German Wikipedia
        if topic == self.german_topic:
            self.german_edits += 1

    def calculate_aggregations(self):
        """
        Calculates the aggregations per minute

        :return: The global edits per minute and the German edits per minute
        """
        elapsed_minutes = (time.time() - self.start_time) / 60

        # Perform aggregation per minute
        if elapsed_minutes >= 1:
            global_edits_per_minute = self.global_edits / elapsed_minutes
            german_edits_per_minute = self.german_edits / elapsed_minutes

            # Print and save the results
            self.logger.info(f"Global edits per minute: {global_edits_per_minute}")
            self.logger.info(f"German edits per minute: {german_edits_per_minute}")

            print(f"\nGlobal edits per minute: {global_edits_per_minute}")
            print(f"German edits per minute: {german_edits_per_minute}")

            self.write_aggregations_to_file(
                global_edits_per_minute, german_edits_per_minute
            )


            # Reset counters and start time
            self.global_edits = 0
            self.german_edits = 0
            self.start_time = time.time()

            return global_edits_per_minute, german_edits_per_minute
        else:
            # Return 0 edits per minute if no new messages are received
            return 0, 0

    def consume_messages(self):
        """
        Consumes messages from Kafka topics
        """
        self.global_edits = 0
        self.german_edits = 0
        self.start_time = time.time()

        # Subscribe to the topics
        self.consumer.subscribe([self.topic, self.german_topic])

        try:
            # Consume messages
            while True:
                msg = self.consumer.poll(
                    timeout=1
                )  # 1 = max 1 second timeout  > wait max 1 second for new messages before continuing
                
                if msg is None:
                    # No new messages received, calculate aggregations and return 0 if necessary
                    self.calculate_aggregations()
                    continue
                if msg.error():
                    self.logger.error("Error: {}".format(msg.error()))
                    continue

                # Print a dot for every message (for debugging purposes)
                print(".", end="")
                sys.stdout.flush()

                self.process_message(msg)
                self.calculate_aggregations()

        except KeyboardInterrupt:
            self.logger.info("%% Aborted by user\n")

    def close(self):
        """
        Closes the Kafka consumer
        """
        self.consumer.close()

    def run(self):
        """
        Runs the Kafka consumer
        """
        try:
            self.consume_messages()

        finally:
            self.close()


if __name__ == "__main__":
    consumer = KafkaConsumer()
    consumer.run()
