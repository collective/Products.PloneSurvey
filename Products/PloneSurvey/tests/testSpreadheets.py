import unittest

from DateTime import DateTime

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from base import INTEGRATION_TESTING
from base import fixLineEndings


class TestBuildSpreadsheetFilename(unittest.TestCase):
    """Ensure spreadsheet 2 works"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')

    def testSpreadsheetFilename(self):
        s1 = getattr(self, 's1')
        today = DateTime().strftime("%Y-%m-%d")
        expected_spreadsheet_filename = s1.getId() + '-' + today + '.csv'
        spreadsheet_filename = s1.buildSpreadsheetUrl()
        assert spreadsheet_filename == expected_spreadsheet_filename, \
            "Filename incorrect: %s - %s" % (spreadsheet_filename,
                                             expected_spreadsheet_filename)


class TestSpreadsheet2(unittest.TestCase):
    """Ensure spreadsheet 2 works"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testReturnNothing(self):
        s1 = getattr(self, 's1')
        csv_file = s1.buildSpreadsheet2()
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        assert csv_list[1] == '', "More than header row returned"

    def testReturnSomething(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet2()
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        assert "Yes" in csv_list[1], "Answer not in file"

    def testUerName(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet2()
        assert "test_user_1_" in csv_file, "User name not in spreadsheet"


class TestSpreadsheet3(unittest.TestCase):
    """Ensure spreadsheet 3 works"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testReturnNothing(self):
        s1 = getattr(self, 's1')
        csv_file = s1.buildSpreadsheet3()
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        assert csv_list[1] == '', "More than header row returned"

    def testReturnSomething(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet3()
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        assert "0" in csv_list[1], "Answer not in file"

    def testUerName(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet3()
        assert "test_user_1_" in csv_file, "User name not in spreadsheet"


class TestSelectInSpreadsheet(unittest.TestCase):
    """Ensure select question in spreadsheets works"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testReturnAnswer(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSpreadsheet2()
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        assert "Yes" in csv_list[1], "Answer not in file"
        csv_file = s1.buildSpreadsheet3()
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        assert "0" in csv_list[1], "Answer not in file"


class TestSummarySpreadsheet(unittest.TestCase):
    """Ensure summary spreadsheet returns correct results"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testReturnAnswer(self):
        s1 = getattr(self, 's1')
        csv_file = s1.buildSummarySpreadsheet()
        assert csv_file is not None


class TestSelectSpreadsheet(unittest.TestCase):
    """Ensure select spreadsheet returns correct results"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')

    def testReturnSomething(self):
        s1 = getattr(self, 's1')
        csv_file = s1.buildSelectSpreadsheet()
        assert csv_file is not None

    def testReturnSingleAnswer(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer('Yes')
        csv_file = s1.buildSelectSpreadsheet()
        assert csv_file is not None
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        assert "Yes" in csv_list[2], "Answer not in file"

    def testReturnMultipleAnswer(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.addAnswer(['Yes', 'No'])
        csv_file = s1.buildSelectSpreadsheet()
        assert csv_file is not None
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        assert "Yes" in csv_list[2], "Answer not in file"
