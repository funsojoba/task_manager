from datetime import datetime
from rest_framework.exceptions import ValidationError

def validate_date(date_str):
    """
    Validates the date string and returns a datetime object if valid.
    Raises ValidationError if the date is invalid.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(f"Invalid date format: {date_str}. Expected format is YYYY-MM-DD.")
