#
# Test PloneSurvey Survey
#

import os, sys
from DateTime import DateTime
#from AccessControl import Unauthorized
from Testing.makerequest import makerequest
from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from base import PloneSurveyTestCase

class TestBuildSpreadsheetFilename(PloneSurveyTestCase):
    """Ensure spreadsheet 2 works"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')

    def testSpreadsheetFilename(self):
        s1 = getattr(self, 's1')
        today = DateTime().strftime("%Y-%m-%d")
        expected_spreadsheet_filename = s1.getId() + '-' + today + '.csv'
        spreadsheet_filename = s1.buildSpreadsheetUrl()
        assert spreadsheet_filename == expected_spreadsheet_filename, "Filename incorrect: %s - %s" % (spreadsheet_filename, expected_spreadsheet_filename)

class TestSpreadsheet2(PloneSurveyTestCase):
    """Ensure spreadsheet 2 works"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testReturnNothing(self):
        s1 = getattr(self, 's1')
        csv_file = s1.buildSpreadsheet2()
        assert len(csv_file) == 17, "More than header row returned"

    def testReturnSomething(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet2()
        assert len(csv_file) == 49, "More than one row returned"

    def testUerName(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet2()
        assert "test_user_1_" in csv_file, "User name not in spreadsheet"

class TestSpreadsheet3(PloneSurveyTestCase):
    """Ensure spreadsheet 3 works"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testReturnNothing(self):
        s1 = getattr(self, 's1')
        csv_file = s1.buildSpreadsheet3()
        assert len(csv_file) == 17, "More than header row returned"

    def testReturnSomething(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet3()
        assert len(csv_file) == 47, "More than one row returned"

    def testUerName(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet3()
        assert "test_user_1_" in csv_file, "User name not in spreadsheet"

class TestSelectInSpreadsheet(PloneSurveyTestCase):
    """Ensure select question in spreadsheets works"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testReturnAnswer(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet2()
        assert "Yes" in csv_file, "Answer not in file"
        csv_file = s1.buildSpreadsheet3()
        assert "0" in csv_file, "Answer not in csv file"

class TestSummarySpreadsheet(PloneSurveyTestCase):
    """Ensure summary spreadsheet returns correct results"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testReturnAnswer(self):
        s1 = getattr(self, 's1')
        csv_file = s1.buildSummarySpreadsheet()
        assert csv_file is not None

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBuildSpreadsheetFilename))
    suite.addTest(makeSuite(TestSpreadsheet2))
    suite.addTest(makeSuite(TestSpreadsheet3))
    suite.addTest(makeSuite(TestSelectInSpreadsheet))
    suite.addTest(makeSuite(TestSummarySpreadsheet))
    return suite
