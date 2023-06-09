import sys
import pytest
import io
import csv

# add the src directory to the path
sys.path.append("src")
from src.libs.helper import load_schema, check_schema, encode_failed


# ############################
# ##### LOAD SCHEMA TESTS ####
# ############################
def test_load_schema():
    """
    test_load_schema Checks if load_schema works
    Expected: schema is a dict
    """
    schema = load_schema("tests/static/wikipedia-schema.json")
    assert schema["type"] == "object"


def test_load_schema_failed():
    """
    test_load_schema_failed Checks if load_schema fails
    Expected: FileNotFoundError
    """
    with pytest.raises(FileNotFoundError):
        load_schema("tests/static/wikipedia-schema2.json")


# ############################
# ##### CHECK SCHEMA TESTS ####
# ############################


def test_check_schema():
    """
    test_check_schema Checks if check_schema works
    Expected: True
    """
    # Load the schema
    schema = load_schema("tests/static/wikipedia-schema.json")

    # CSV rows from the example file
    with open("tests/data/data-correct.csv", encoding="utf-8") as csvfile:
        # read csv file
        reader = csv.DictReader(csvfile, delimiter=",")

        for row in reader:
            assert check_schema(row, schema) == True


def test_check_schema_fail():
    """
    test_check_schema_fail Checks if check_schema fails
    > In the data the second row is not following the predefined schema, so the check should fail
    Expected: False
    """

    # Load the schema
    schema = load_schema("tests/static/wikipedia-schema.json")

    # CSV rows from the example file
    with open("tests/data/data-failed.csv", encoding="utf-8") as csvfile:
        # read csv file
        reader = csv.DictReader(csvfile, delimiter=",")

        assert check_schema(next(reader), schema) == True  # first row is valid
        assert check_schema(next(reader), schema) == False  # second row is invalid
        assert check_schema(next(reader), schema) == True  # third row is valid
