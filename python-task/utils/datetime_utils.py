from datetime import datetime

from dateutil.relativedelta import relativedelta


def string_to_date(date_str: str) -> datetime.date:
    """
    Converts string in YY/MM/DD or YY-MM-DD format to date object.

    Parameters
    ----------
    date_str : str
        The date as string.

    Returns
    -------
    date_obj : datetime.date
        Date object.
    """
    if "-" in date_str:
        date_format = "%Y-%m-%d"
    else:
        date_format = "%Y/%m/%d"

    date_obj = datetime.strptime(date_str, date_format).date()
    return date_obj


def get_months_diff_between_dates(start_date: datetime.date, end_date: datetime.date):
    """
    Calculates months between two dates.

    Parameters
    ----------
    start_date : datetime.date
        Start date.
    end_date: datetime.date
        End date.

    Returns
    -------
    months_diff : int
        Months between the two dates.
    """
    delta = relativedelta(end_date, start_date)
    months_diff = 12 * delta.years + delta.months
    return months_diff
