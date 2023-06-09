import pytest
import os
import csv
from unittest import mock
from confluent_kafka import Consumer
from src.structured import StructuredZoneConsumer


def test_write_aggregations_to_file(mocker):
    consumer = StructuredZoneConsumer()

    file_path = "test.csv"
    mocker.patch.dict(os.environ, {"AGGREGATION_FILE_PATH": file_path})

    global_edits_per_minute = 10
    german_edits_per_minute = 5

    # Remove the file if it exists
    if os.path.isfile(file_path):
        os.remove(file_path)

    consumer.write_aggregations_to_file(
        global_edits_per_minute, german_edits_per_minute
    )

    assert os.path.isfile(file_path)

    with open(file_path, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

        assert len(rows) == 2  # Header + 1 data row

        header = rows[0]
        assert header == [
            "timestamp",
            "global_edits_per_minute",
            "german_edits_per_minute",
        ]

        data_row = rows[1]
        timestamp, global_edits, german_edits = data_row
        assert timestamp != ""
        assert global_edits == str(global_edits_per_minute)
        assert german_edits == str(german_edits_per_minute)


def test_process_message():
    consumer = StructuredZoneConsumer()

    message = mock.Mock()
    message.topic.return_value = "wikipedia-success"
    message.value.return_value.decode.return_value = "test message"

    consumer.process_message(message)

    assert consumer.global_edits == 1
    assert consumer.german_edits == 0

    message.topic.return_value = "wikipedia-dewiki-success"
    consumer.process_message(message)

    assert consumer.global_edits == 1
    assert consumer.german_edits == 1


def test_calculate_aggregations(mocker):
    consumer = StructuredZoneConsumer()

    mocker.patch("time.time", return_value=100)
    consumer.start_time = 0
    consumer.global_edits = 10
    consumer.german_edits = 5

    global_edits_per_minute, german_edits_per_minute = consumer.calculate_aggregations()

    assert global_edits_per_minute == 6
    assert german_edits_per_minute == 3

    assert consumer.global_edits == 0
    assert consumer.german_edits == 0
    assert consumer.start_time == 100
