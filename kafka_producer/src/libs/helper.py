import json
from jsonschema import validate, exceptions


def check_schema(data, schema):
    """
    check_schema Checks if data is valid json and follows the schema

    :param data: The data to check
    :param schema: The schema to check against
    :return: True if valid, False if not
    """

    # check if data is following the schema
    try:
        validate(data, schema)
    except exceptions.ValidationError as e:
        return False

    return True


def load_schema(path):
    """
    load_schema Loads a schema from a path

    :param path: The path to the schema
    :return: The schema
    """
    with open(path) as file:
        schema = json.load(file)

    return schema


def encode_failed(data):
    """
    encode_failed Encodes failed data in json object

    :param data: The data to encode
    :return: The encoded data
    """
    obj = {"failed": True, "data": data}
    return json.dumps(obj)
