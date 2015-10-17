import unittest

from plone.app.testing import TEST_USER_ID, setRoles

from base import INTEGRATION_TESTING, INTEGRATION_BRANCHING_TESTING


class TestBranchingConditions(unittest.TestCase):
    """Test Survey Branching fields"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        s1 = getattr(self.portal, 's1')
        s1.invokeFactory('Survey Select Question', 'ssq1')
        s1.invokeFactory('Sub Survey', 'ss1')
        s1.invokeFactory('Sub Survey', 'ss2')

    def testEditSubSurveyBranch(self):
        s1 = getattr(self.portal, 's1')
        ss1 = getattr(s1, 'ss1')
        ss1.setRequiredQuestion('ssq1')
        ss1.setRequiredAnswer(1)
        self.assertEqual(ss1.getRequiredQuestion(), 'ssq1')
        self.assertEqual(ss1.getRequiredAnswer(), 1)

    def testSingleBranchChoice(self):
        s1 = getattr(self.portal, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ss1 = getattr(s1, 'ss1')
        ss2 = getattr(s1, 'ss2')
        ssq1.addAnswer('Yes')
        ss1.setRequiredQuestion('ssq1')
        ss1.setRequiredAnswer(1)
        ss2.setRequiredQuestion('ssq1')
        ss2.setRequiredAnswer(0)


class TestRadioBranching(unittest.TestCase):
    """Test Survey Branching for radio questions"""
    layer = INTEGRATION_BRANCHING_TESTING

    def setUp(self):
        """Create a survey with four pages"""
        self.portal = self.layer['portal']
        self.s1 = getattr(self.portal, 's1')
        self.layer['request'].set('ACTUAL_URL', self.s1.absolute_url())

    def testNoAnswers(self):
        """No answer added, so survey exits"""
        next_page = self.s1.getNextPage()
        assert not self.s1.ss1.displaySubSurvey()
        assert next_page == 'http://nohost/plone/'

    def testNoAnswersNegative(self):
        """No answer added, survey should exit"""
        self.s1.ss2.setRequiredAnswerYesNo(0)
        next_page = self.s1.getNextPage()
        assert not self.s1.ss1.displaySubSurvey()
        assert next_page == 'http://nohost/plone/'

    def testAnswerNo(self):
        """S1 as no should return ss1"""
        self.s1.ssq1.addAnswer('No')
        next_page = self.s1.getNextPage()
        assert self.s1.ss1.displaySubSurvey()
        assert '<base href="http://nohost/plone/s1/ss1/" />' in next_page

    def testAnswerYes(self):
        """S1 as yes should return ss2"""
        self.s1.ssq1.addAnswer('Yes')
        next_page = self.s1.getNextPage()
        assert not self.s1.ss1.displaySubSurvey()
        assert self.s1.ss2.displaySubSurvey()
        assert '<base href="http://nohost/plone/s1/ss2/" />' in next_page


class TestSubSurveyRadioBranching(unittest.TestCase):
    """Test sub survey Branching for radio questions"""
    layer = INTEGRATION_BRANCHING_TESTING

    def setUp(self):
        """Create a survey with four pages"""
        self.portal = self.layer['portal']
        self.ss1 = getattr(self.portal.s1, 'ss1')
        self.ss2 = getattr(self.portal.s1, 'ss2')

    def testNoAnswers(self):
        """No answer added, so survey exits"""
        next_page = self.ss1.getNextPage()
        assert not self.ss1.displaySubSurvey()
        assert next_page == 'http://nohost/plone/'

    def testNoAnswersNegative(self):
        """No answer added, so survey exits"""
        self.ss2.setRequiredAnswerYesNo(0)
        next_page = self.ss1.getNextPage()
        assert not self.ss1.displaySubSurvey()
        assert next_page == 'http://nohost/plone/'

    def testAnswerNo(self):
        """S1 as no should exit survey"""
        self.ss1.ssq2.addAnswer('No')
        next_page = self.ss1.getNextPage()
        assert not self.ss1.displaySubSurvey()
        assert next_page == 'http://nohost/plone/', next_page

    def testAnswerYes(self):
        """ss1 as yes should return ss3"""
        self.ss1.ssq2.addAnswer('Yes')
        # next_page = self.ss1.getNextPage()
        # assert not self.ss3.displaySubSurvey()
        # assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss3/" />' in next_page


class TestCheckboxBranching(unittest.TestCase):
    """Test Survey Branching for radio questions"""
    layer = INTEGRATION_BRANCHING_TESTING

    def setUp(self):
        """Create a survey with four pages"""
        self.portal = self.layer['portal']
        self.s1 = getattr(self.portal, 's1')
        self.s1.ssq1.setInputType('checkbox')
        self.layer['request'].set('ACTUAL_URL', self.s1.absolute_url())

    def testAnswerNo(self):
        """S1 as no should return ss1"""
        self.s1.ssq1.addAnswer('No')
        next_page = self.s1.getNextPage()
        assert self.s1.ss1.displaySubSurvey()
        assert '<base href="http://nohost/plone/s1/ss1/" />' in next_page

    def testAnswerYes(self):
        """S1 as yes should exit survey"""
        self.s1.ssq1.addAnswer('Yes')
        next_page = self.s1.getNextPage()
        assert not self.s1.ss1.displaySubSurvey()
        assert '<base href="http://nohost/plone/s1/ss2/" />' in next_page

    def testAnswerList(self):
        """S1 with yes should return ss1"""
        self.s1.ssq1.addAnswer(['Yes', 'No'])
        next_page = self.s1.getNextPage()
        assert self.s1.ss1.displaySubSurvey()
        assert '<base href="http://nohost/plone/s1/ss1/" />' in next_page, \
            next_page[next_page.find('<base href'):
                      next_page.find('<base href')+100]


class TestSubSurveyCheckboxBranching(unittest.TestCase):
    """Test sub survey Branching for checkbox questions"""
    layer = INTEGRATION_BRANCHING_TESTING

    def setUp(self):
        """Create a survey with four pages"""
        self.portal = self.layer['portal']
        self.s1 = getattr(self.portal, 's1')
        self.ss1 = getattr(self.s1, 'ss1')
        self.ss2 = getattr(self.s1, 'ss2')
        self.ss1.ssq2.setInputType('checkbox')

    def testAnswerNo(self):
        """ss1 as no should return ss1"""
        self.ss1.ssq2.addAnswer('No')
        next_page = self.ss1.getNextPage()
        assert not self.ss2.displaySubSurvey()
        assert next_page == 'http://nohost/plone/', next_page

    def testAnswerYes(self):
        """ss1 as yes should return ss3"""
        self.ss1.ssq2.addAnswer('Yes')
        # next_page = self.ss1.getNextPage()
        assert not self.ss2.displaySubSurvey()
        # assert self.ss3.displaySubSurvey()
        # assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss3/" />' in next_page

    def testAnswerList(self):
        """ss1 with yes should return ss1"""
        self.ss1.ssq2.addAnswer(['Yes', 'No'])
        # next_page = self.ss1.getNextPage()
        # assert self.ss3.displaySubSurvey()
        # assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss3/" />' in next_page, next_page[next_page.find('<base href'):next_page.find('<base href')+100]
