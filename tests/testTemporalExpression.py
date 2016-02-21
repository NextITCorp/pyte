import unittest as ut
import datetime as dt
import pytz as tz
import pyte.TemporalExpressions as te
import pyte.DateExtensions as de

class TestTemporalExpression(ut.TestCase):

    def testDayInMonthIncludesDate(self):
        dt1 = dt.datetime(2015,12,1,0,0,0, tzinfo = tz.utc)
        teFunc = te.dayInMonth(2,0)
        self.assertTrue(teFunc(dt1))

    def testDayInMonthRequiresUtcDate(self):
        dt1 = dt.datetime(2015,12,1,0,0,0)
        teFunc = te.dayInMonth(2,0)
        self.assertRaises(ValueError, teFunc, dt1)

    def testDayInMonthSelectsLastTuesdayOfMonth(self):
        dt1 = dt.datetime(2015,12,29,0,0,0, tzinfo = tz.utc)
        teFunc = te.dayInMonth(2,-1)
        self.assertTrue(teFunc(dt1))

    def testCheckUtcDateThrowsIfNotUtc(self):
        dt1 = dt.datetime(2015,12,1,0,0,0)
        dt2 = dt.datetime(2015,12,29,0,0,0, tzinfo = tz.utc)
        self.assertRaises(ValueError, te.checkUtcDate, dt1)
        self.assertTrue(te.checkUtcDate(dt2))

    def testRangeInYearContainsDate(self):
        dt1 = dt.datetime(2015,2,22,0,0,0, tzinfo = tz.utc)
        fnt = te.rangeInYear(1,1,4,1)
        self.assertTrue(fnt(dt1))

    def testRangeInYearSelectsDatesInStartMonth(self):
        fnt = te.rangeInYear(1,15,4,10)
        dt1 = dt.datetime(2015,1,22,0,0,0, tzinfo = tz.utc)
        dt2 = dt.datetime(2015,1,12,0,0,0, tzinfo = tz.utc)
        self.assertTrue(fnt(dt1))
        self.assertFalse(fnt(dt2))

    def testRangeInYearSelectsDatesInEndMonth(self):
        fnt = te.rangeInYear(1,15,4,10)
        dt1 = dt.datetime(2015,4,22,0,0,0, tzinfo = tz.utc)
        dt2 = dt.datetime(2015,4,2,0,0,0, tzinfo = tz.utc)
        self.assertFalse(fnt(dt1))
        self.assertTrue(fnt(dt2))

    def testRangeInYearSelectsWhenStartAndEndInOneMonth(self):
        fnt = te.rangeInYear(4,5,4,20)
        dt1 = dt.datetime(2015,4,22,0,0,0, tzinfo = tz.utc)
        dt2 = dt.datetime(2015,4,2,0,0,0, tzinfo = tz.utc)
        dt3 = dt.datetime(2015,4,12,0,0,0, tzinfo = tz.utc)
        dt4 = dt.datetime(2015,4,7,0,0,0, tzinfo = tz.utc)
        self.assertFalse(fnt(dt1))
        self.assertFalse(fnt(dt2))
        self.assertTrue(fnt(dt3))
        self.assertTrue(fnt(dt4))


    def testTESequenceSelectsAnyMemberThatAppliesToTheDate(self):
        # first tuesday and last friday of the month
        fnt = te.temporalExpressionSequence([ \
                te.dayInMonth(2,0) \
                ,te.dayInMonth(5,-1) \
                ])
        dtApplies1 = dt.datetime(2015,12,25,0,0,0,tzinfo=tz.utc)
        dtApplies2 = dt.datetime(2015,2,3,0,0,0,tzinfo=tz.utc)
        dtDoesNotApply1 = dt.datetime(2015,2,4,0,0,0,tzinfo=tz.utc)
        self.assertTrue(fnt(dtApplies1))
        self.assertTrue(fnt(dtApplies2))
        self.assertFalse(fnt(dtDoesNotApply1))

    def testTEIntersectionSelectsOnlyIfDateMatchesAllConditions(self):
        # Tuesday and Friday in March
        fnt = te.temporalExpressionIntersection([ \
                te.temporalExpressionSequence([ \
                    te.dayOfWeek(2), te.dayOfWeek(5)]) \
                , te.rangeInYear(3,1,3,31)])
        dtApplies1 = dt.datetime(2015,3,24,0,0,0,tzinfo=tz.utc)
        dtApplies2 = dt.datetime(2015,3,6,0,0,0,tzinfo=tz.utc)
        dtDoesNotApply1 = dt.datetime(2015,2,4,0,0,0,tzinfo=tz.utc)
        dtDoesNotApply2 = dt.datetime(2015,3,4,0,0,0,tzinfo=tz.utc)
        self.assertTrue(fnt(dtApplies1))
        self.assertTrue(fnt(dtApplies2))
        self.assertFalse(fnt(dtDoesNotApply1))
        self.assertFalse(fnt(dtDoesNotApply2))

    def testTEDifferenceExcludesWeekends(self):
        # Excludes weekends from dates
        fnt = te.temporalExpressionDifference( \
                te.rangeInYear(3,1,3,31)
                , te.temporalExpressionSequence([ \
                    te.dayOfWeek(0), te.dayOfWeek(6)]))
        dtApplies1 = dt.datetime(2015,3,24,0,0,0,tzinfo=tz.utc)
        dtApplies2 = dt.datetime(2015,3,6,0,0,0,tzinfo=tz.utc)
        dtDoesNotApply1 = dt.datetime(2015,2,4,0,0,0,tzinfo=tz.utc)
        dtDoesNotApply2 = dt.datetime(2015,3,7,0,0,0,tzinfo=tz.utc)
        dtDoesNotApply3 = dt.datetime(2015,3,29,0,0,0,tzinfo=tz.utc)
        self.assertTrue(fnt(dtApplies1))
        self.assertTrue(fnt(dtApplies2))
        self.assertFalse(fnt(dtDoesNotApply1))
        self.assertFalse(fnt(dtDoesNotApply2))
        self.assertFalse(fnt(dtDoesNotApply3))

    def testGenerateAllWorkDaysInMarch(self):
        fnt = te.temporalExpressionDifference( \
                te.rangeInYear(3,1,4,1)
                , te.temporalExpressionSequence([ \
                    te.dayOfWeek(0), te.dayOfWeek(6)]))
        dateList = [d for d in de.dateRangeGenerator( \
                dt.datetime(2015,3,1,0,0,0, tzinfo=tz.utc) \
                ,dt.datetime(2015,4,1,0,0,0, tzinfo=tz.utc)) \
                if fnt(d)]
        self.assertEqual(dateList[0], dt.datetime(2015,3,2,0,0,0, tzinfo=tz.utc))
        self.assertEqual(dateList[-1], dt.datetime(2015,3,31,0,0,0, tzinfo=tz.utc))
        self.assertEqual(len(dateList), 22)

