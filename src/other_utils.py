from datetime import datetime
from collections import OrderedDict


def get_datetime_from_timestamp(timestamp):
    """
    From the doc: https://riot-api-libraries.readthedocs.io/en/latest/specifics.html
    "The creation date timestamps in milliseconds (not seconds)."

    Returns: datetime object
    """
    return datetime.fromtimestamp(timestamp / 1000)


def sort_ordered_dict(d, key, reverse=False):
    """
    Returns a sorted OrderedDict based on the value of the provided key
    """
    return OrderedDict(
        sorted(
            d.items(),
            key=lambda key_value_pair: key_value_pair[1][key],
            reverse=reverse,
        )
    )
