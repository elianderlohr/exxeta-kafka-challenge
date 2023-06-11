import sys
import json
import pytest
from confluent_kafka import Consumer

# add the src directory to the path
sys.path.append("src")
from src.kafka_producer import KafkaProducer


def test_produce_message():
    """
    test_produce_message Checks if produce_message works
    Expected: No Exception
    """

    # create a producer
    landing_zone = KafkaProducer(dotenv_path="tests/.env")

    # create a producer
    landing_zone.create_producer()

    # producer message and make sure no Error got thrown
    try:
        landing_zone.produce_message("test", json.dumps({"test": True}))
    except Exception as e:
        pytest.fail("Exception was thrown: {}".format(e))


def test_produce_csv_messages():
    """
    test_produce_csv_messages Checks if produce_csv_messages works for only correct data
    Expected: 4 topics are created
    """

    # create a producer
    landing_zone = KafkaProducer(dotenv_path="tests/.env")

    # create a producer
    landing_zone.create_producer()

    # Path to the csv file
    data_path = "tests/data/data-correct.csv"

    # Parse the csv file and produce the messages
    landing_zone.produce_csv_messages(data_path)

    # Create consumer to check if the messages were produced
    consumer = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": "test",
            "auto.offset.reset": "earliest",
        }
    )

    expected_topics = [
        "wikipedia-success",
        "wikipedia-jawiki-success",
        "wikipedia-nlwiki-success",
        "wikipedia-wikidatawiki-success",
    ]

    topics = list(dict(consumer.list_topics().topics).keys())

    print(topics)
    # Check if the expected_topics are in the topics (as key)
    for topic in expected_topics:
        assert topic in topics


def test_produce_csv_message_error_message():
    """
    test_produce_csv_messages Checks if produce_csv_messages works and messages with wrong schema get produce to failed topic
    Expected: 1 error topic is created
    """

    # create a producer
    landing_zone = KafkaProducer(dotenv_path="tests/.env")

    # create a producer
    landing_zone.create_producer()

    # Path to the csv file
    data_path = "tests/data/data-failed.csv"

    # Parse the csv file and produce the messages
    landing_zone.produce_csv_messages(data_path)

    # Create consumer to check if the messages were produced
    consumer = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": "test",
            "auto.offset.reset": "earliest",
        }
    )
    

    expected_topics = [
        "wikipedia-success",
        "wikipedia-jawiki-success",
        "wikipedia-failed-schema",
        "wikipedia-wikidatawiki-success",
    ]

    topics = list(dict(consumer.list_topics().topics).keys())

    print(topics)
    # Check if the expected_topics are in the topics (as key)
    for topic in expected_topics:
        assert topic in topics
