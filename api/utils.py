import datetime
import decimal


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
    column_names = rows[0]._mapping
    return [convert_to_dict(row, column_names) for row in rows]
    # return [dict(row._mapping) for row in rows]


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
