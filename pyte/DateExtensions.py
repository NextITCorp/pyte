"""
DateExtensions.py - Useful functions for date processing.
"""

import datetime as dt
import pytz as tz

def isUtc(theDateTime):
    """
    does a date have utc timezone?
    :param theDateTime: A date to check for utc timezone
    :return: True if the date has utc timezone,
             False if the date has no timezone 
             or the timezone is not utc.
    """
    return theDateTime.tzname() == 'UTC'

def dateRangeGenerator(startDate, endDate):
    """
    Generate a range of dates between startDate and endDate.  
    The endDate is excluded from the range.
    :param startDate: The first date in the range.
    :param endDate: The day after the last day in the range.
    :return: a generator over the specified range.
    """
    if not isUtc(startDate) or not isUtc(endDate):
        raise ValueError('dates must be Utc')

    length = int((endDate-startDate)/dt.timedelta(days=1))
    for dist in range(length):
        yield startDate+dt.timedelta(days=dist)

def dateRange(startDate, endDate):
    """
    generate a list of dates in a range.
    :param startDate: The first date in the range.
    :param endDate: The day after the last day in the range.
    :return: a list of dates in the range.
    """
    return list(dateRangeGenerator(startDate, endDate))

