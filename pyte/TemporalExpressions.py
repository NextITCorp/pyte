"""
TemporalExpression.py - a pattern builder for 
   determining whether dates or times are in a schedule.
       For example, use TE to tell if a date is the 
       second Tuesday of a month between January and March.

   Each function takes the parameters needed to create a 
   closure that contains the predicate function.
"""

from functools import reduce
from operator import and_, or_
import datetime as dt
import pytz as tz
import calendar as cal
from .DateExtensions import isUtc,dateRangeGenerator

def dayInMonth(dayOfWeek, weekInMonth):
    """
    Create a temporal expression that matches on a particular weekday 
    in a month.
    :param dayOfWeek: An int between 0 (Sunday) and 6 (Saturday)
    :param weekInMonth: An int from 0 to the number of weeks in 
                        the month, or -1 for the last week of the 
                        month.
    :return: a predicate function to evaluate whether or not a date is 
            on a particular weekday in a week of a month (e.g, first
            Monday, or last Friday, etc)
    """
    def includes(candidate):
        """
        Evaluate if a date is a day in a week (e.g.,second Tuesday 
        in the month).
        :param: A datetime value to check.
        :return: A boolean indicating whether or not the date is 
                included in the temporal expression.  For example,
                is the date the first Monday of the Month?
        """
        checkUtcDate(candidate)
        return dayMatches(candidate, dayOfWeek) and \
                weekInMonthMatches(candidate, weekInMonth)
    return includes

def dayOfWeek(dayInWeek):
    """
    Create a temporal expression to evaluate if a date is on a 
    particular weekday.
    :param dayInWeek: An int between 0 (Sunday) and 6 (Saturday)
    :return: A predicate function to evaluate if a date occurs on 
            the specified weekday.
    """
    def includes(candidate):
        """
        Evaluate if a date is on the specified weekday.
        :param: A datetime value to check.
        :return: A boolean indicating whether or not the date is 
                included in the temporal expression.  For example,
                is the date a Monday?
        """
        checkUtcDate(candidate)
        return dayMatches(candidate, dayInWeek)
    return includes

def rangeInYear(startMonth, startDay, endMonth, endDay):
    """
    Specify a range of days that are in a temporal expression.  
    The range is defined with a start month and day and an end
    month and day.  Then it is possible to repeat the range for 
    mutiple years if necessary.
    :param startMonth: An int from 1 (January) to 12 (December) 
                    representing a start month for the range.
    :param startDay: An int representing the day in the month 
                    that is the first day of the range.
    :param endMonth: An int from 1 (January) to 12 (December) 
                    representing an end month for the range.
    :param endDay: An int representing the day in the month 
                    that is the day after the last day of the range.
    """
    def includes(candidate):
        checkUtcDate(candidate)
        if startMonth == endMonth:
            return candidate.month == startMonth \
               and startDay <= candidate.day < endDay
        return (candidate.month > startMonth  and candidate.month < endMonth) \
            or (candidate.month == startMonth and candidate.day >= startDay) \
            or (candidate.month == endMonth   and candidate.day < endDay)
    return includes

def temporalExpressionSequence(teList):
    """
    Create a predicate temporal expression that combines the results 
    of a sequence of temporal expressions into a single expression.  
    The returned expression will evaluate to True if any expression 
    in the list evaluates to True.
    :param teList: A list of temporal expression predicates.
    :returns: A predicate that evaluates the temporal expression.
    """
    def includes(candidate):
        checkUtcDate(candidate)
        return any(tefunc(candidate) for tefunc in teList)
    return includes

def temporalExpressionIntersection(teList):
    """
    Create a predicate temporal expression that combines the results 
    of a sequence of temporal expressions into a single expression.  
    The returned expression will evaluate to True if all expressions 
    in the list evaluate to True.
    :param teList: A list of temporal expression predicates.
    :returns: A predicate that evaluates the temporal expression.
    """
    def includes(candidate):
        checkUtcDate(candidate)
        return all(tefunc(candidate) for tefunc in teList)
    return includes

def temporalExpressionDifference(teInclude, teExclude):
    """
    Create a predicate temporal expression that combines the results 
    of a sequence of temporal expressions into a single expression.  
    The returned expression will evaluate to True if the first 
    expression in the list evaluates to True and the second 
    evaluates to False.
    :param teInclude: A temporal expression predicate that should 
                    be True for the predicate to evaluate to True.
    :param teExclude: A temporal expression predicate that should 
                    be False for the predicate to evaluate to True.
    :returns: A predicate that evaluates the temporal expression.
    """
    def includes(candidate):
        checkUtcDate(candidate)
        return teInclude(candidate) and not teExclude(candidate)
    return includes

def checkUtcDate(candidate):
    """
    Check if a date is Utc.  raise ValueError exception if the 
    date is not utc.
    :param candidate: The date to check
    :return: True if the date is utc.  otherwise,
    :raises: A ValueError exception.
    """
    if not isUtc(candidate): 
        raise ValueError('Date must be UTC')
    return True

# TODO: move to a new module
# helper functions
def dayMatches(candidate, dayInWeek):
    return candidate.isoweekday()%7 == dayInWeek

def weekInMonthMatches(candidate, weekInMonth):
    if weekInMonth >= 0:
        return (candidate.day-1)//7 == weekInMonth
    return (cal.monthrange(candidate.year, \
            candidate.month)[1]-candidate.day)//7 \
            == weekInMonth +1

