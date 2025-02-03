import datetime
import decimal
import re

from flask import request, abort
from sqlalchemy.orm import class_mapper

def normalize(element: str) -> str:
    """
    Normalize the element by converting it to uppercase and replacing the underscores by spaces.
    :param element:
    :return:
    """
    return element.upper().replace("_", " ") if element is not None else None


def as_dict(obj):
    data = obj.__dict__
    if '_sa_instance_state' in data:
        data.pop('_sa_instance_state')
    return data.copy()


def from_dict(self, data):
    for field in data:
        if field in self.__table__.columns:
            setattr(self, field, data[field])

def row_to_dict(row):
    """Converts a SQLAlchemy row object to a dictionary."""
    return convert_to_dict(row, row._fields)

def to_dict(rows):
    """
    Convert a SQLAlchemy result to a list of dictionaries.
    :param rows:
    :return:
    """
    if not rows:
        return None
    if len(rows) == 0:
        return rows

    return [row.as_dict() for row in rows]


def convert_to_dict(row, column_names):
    """
    Convert a SQLAlchemy row and column names to a dictionary,
    converting datetime objects to ISO format.
    """
    result = {}
    for key, value in zip(column_names, row):
        result[key] = valid_value(value)
    return result


def valid_value(value):
    """
    Convert the value to a valid string format.
    :param value: the value to be converted.
    :return:
    """
    if isinstance(value, (datetime.date, datetime.time, datetime.datetime)):
        return value.isoformat()
    elif isinstance(value, datetime.timedelta):
        return str(value)
    elif isinstance(value, decimal.Decimal):
        return str(value)
    else:
        return value


# Define a custom function to serialize datetime objects

def serialize_datetime(value):
    if isinstance(value, (datetime.date, datetime.time, datetime.datetime)):
        return value.isoformat()
    elif isinstance(value, datetime.timedelta):
        return str(value)
    elif isinstance(value, decimal.Decimal):
        return str(value)
    return value

    # raise TypeError("Type not serializable")

def commas_to_dot(value: str):
    """
    Replace commas with dots in a string. Also removes all leading and trailing whitespace.
    That is, it converts 1,234,567.89 into 1234567.89 and 3,14 into 3.14 it also converts 3.14 into 3.14
    and 1,234,567 into 1234.567
    :param value:
    :return:
    """
    result = value.strip()
    # Check if the value contains a dot, or a comma. The rightmost represent the decimal part, the leftmost the has
    # to be removed.
    lastdot = result.rfind('.')
    lastcomma = result.rfind(',')
    if lastdot > lastcomma:
        result = result.replace(',', '')
    else:
        result = result.replace(',', '.')
    # remove from result the dots except the last one
    result = result.replace('.', '', result.count('.') - 1)
    return result

def dms_to_decimal(degrees, minutes, seconds, direction):
    # Convert DMS (Degrees, Minutes, Seconds) to decimal format
    number = float(degrees) + float(minutes) / 60.0 + float(seconds) / 3600.0

    # Adjust for hemisphere
    if direction in ['S', 'W']:  # South and West should be negative
        number *= -1

    return number

def convert_to_coordinate(coord_string):
    try:
        # Remove whitespace and any extra symbols (like °, ', " if present)
        coord_string = commas_to_dot(coord_string)

        # Check if it's a decimal value (simple float conversion)
        if re.match(r'^-?\d+(\.\d+)?$', coord_string):
            return float(coord_string)

        # Check if it's in Degrees, Minutes, Seconds format (DMS)
        dms_regex = r'(\d+)[° ]+(\d+)\'[ ]*(\d+(\.\d+)?)[\"\s]*(N|S|E|W)?'
        match = re.match(dms_regex, coord_string)

        if match:
            degrees = match.group(1)
            minutes = match.group(2)
            seconds = match.group(3)
            direction = match.group(5)  # N, S, E, W direction (optional)

            # If no direction is provided, return None (invalid format)
            if not direction:
                return None

            # Convert DMS to decimal
            return dms_to_decimal(degrees, minutes, seconds, direction)

        # If no match, return None (invalid format)
        return None

    except ValueError:
        # Handle cases where conversion fails
        return None
