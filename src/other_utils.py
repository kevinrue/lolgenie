from datetime import datetime


def get_datetime_from_timestamp(timestamp):
    """
    From the doc: https://riot-api-libraries.readthedocs.io/en/latest/specifics.html
    "The creation date timestamps in milliseconds (not seconds)."

    Returns: datetime object
    """
    return datetime.fromtimestamp(timestamp / 1000)
