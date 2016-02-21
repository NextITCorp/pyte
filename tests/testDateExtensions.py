import datetime as dt
import pytz as tz
from pyte.DateExtensions import isUtc,dateRangeGenerator,dateRange

import unittest as ut

class TestDateExtensions(ut.TestCase):

    def testDateObjectIsNotUtcAwareByDefault(self):
        date1 = dt.datetime.now()
        self.assertFalse(isUtc(date1))

    def testDateRangeRequiresUtcDateTime(self):
        date1 = dt.datetime(2015,12,1)
        date2 = dt.datetime(2015,12,15)
        self.assertRaises(ValueError, \
                lambda d1,d2: [d for d in dateRangeGenerator(d1, d2)], date1, date2)

    def testDateRangeAllowsUtcDates(self):
        date1 = dt.datetime(2015,12,1,0,0,0,tzinfo=tz.utc)
        date2 = dt.datetime(2015,12,15,0,0,0,tzinfo=tz.utc)
        dateList = [d for d in dateRangeGenerator(date1, date2)]
        
        self.assertEqual(len(dateList), 14)

    def testEndDateExcludedFromDateRange(self):
        date1 = dt.datetime(2015,12,1,0,0,0,tzinfo=tz.utc)
        date2 = dt.datetime(2015,12,15,0,0,0,tzinfo=tz.utc)
        dateList = [d for d in dateRangeGenerator(date1, date2)]

        self.assertTrue(date2 not in dateList)

    def testMakeSundayZero(self):
        date1 = dt.datetime(2015,6,7,0,0,0,tzinfo=tz.utc)

        self.assertEqual(date1.isoweekday()%7, 0)

if __name__ == '__main__':
    ut.main()
