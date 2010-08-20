#
# Test PloneSurvey Branching
#
from base import PloneSurveyTestCase

class TestBranchingConditions(PloneSurveyTestCase):
    """Test Survey Branching fields"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        s1 = getattr(self.folder, 's1')
        s1.invokeFactory('Survey Select Question', 'ssq1')
        s1.invokeFactory('Sub Survey', 'ss1')
        s1.invokeFactory('Sub Survey', 'ss2')

    def testEditSubSurveyBranch(self):
        s1 = getattr(self.folder, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ss1 = getattr(s1, 'ss1')
        ss2 = getattr(s1, 'ss2')
        ss1.setRequiredQuestion('ssq1')
        ss1.setRequiredAnswer(1)
        self.assertEqual(ss1.getRequiredQuestion(), 'ssq1')
        self.assertEqual(ss1.getRequiredAnswer(), 1)

    def testSingleBranchChoice(self):
        s1 = getattr(self.folder, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ss1 = getattr(s1, 'ss1')
        ss2 = getattr(s1, 'ss2')
        ssq1.addAnswer('Yes')
        ss1.setRequiredQuestion('ssq1')
        ss1.setRequiredAnswer(1)
        ss2.setRequiredQuestion('ssq1')
        ss2.setRequiredAnswer(0)

class TestRadioBranching(PloneSurveyTestCase):
    """Test Survey Branching for radio questions"""

    def afterSetUp(self):
        """Create a survey with four pages"""
        self.createBranchingSurvey()

    def testNoAnswers(self):
        """No answer added, so survey exits"""
        next_page = self.s1.getNextPage()
        assert not self.ss1.displaySubSurvey()
        assert next_page == 'http://nohost/plone/'

    def testNoAnswersNegative(self):
        """No answer added, survey should exit"""
        self.ss2.setRequiredAnswerYesNo(0)
        next_page = self.s1.getNextPage()
        assert not self.ss1.displaySubSurvey()
        assert next_page == 'http://nohost/plone/'

    def testAnswerNo(self):
        """S1 as no should return ss1"""
        self.s1.ssq1.addAnswer('No')
        next_page = self.s1.getNextPage()
        assert self.ss1.displaySubSurvey()
        assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss1/" />' in next_page

    def testAnswerYes(self):
        """S1 as yes should return ss2"""
        self.s1.ssq1.addAnswer('Yes')
        next_page = self.s1.getNextPage()
        assert not self.ss1.displaySubSurvey()
        assert self.ss2.displaySubSurvey()
        assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss2/" />' in next_page

class TestSubSurveyRadioBranching(PloneSurveyTestCase):
    """Test sub survey Branching for radio questions"""

    def afterSetUp(self):
        """Create a survey with four pages"""
        self.createBranchingSurvey()

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
        next_page = self.ss1.getNextPage()
        #assert not self.ss3.displaySubSurvey()
        #assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss3/" />' in next_page

class TestCheckboxBranching(PloneSurveyTestCase):
    """Test Survey Branching for radio questions"""

    def afterSetUp(self):
        """Create a survey with four pages"""
        self.createBranchingSurvey()
        self.s1.ssq1.setInputType('checkbox')

    def testAnswerNo(self):
        """S1 as no should return ss1"""
        self.s1.ssq1.addAnswer('No')
        next_page = self.s1.getNextPage()
        assert self.ss1.displaySubSurvey()
        assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss1/" />' in next_page

    def testAnswerYes(self):
        """S1 as yes should exit survey"""
        self.s1.ssq1.addAnswer('Yes')
        next_page = self.s1.getNextPage()
        assert not self.ss1.displaySubSurvey()
        assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss2/" />' in next_page

    def testAnswerList(self):
        """S1 with yes should return ss1"""
        self.s1.ssq1.addAnswer(['Yes', 'No'])
        next_page = self.s1.getNextPage()
        assert self.ss1.displaySubSurvey()
        assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss1/" />' in next_page, next_page[next_page.find('<base href'):next_page.find('<base href')+100]

class TestSubSurveyCheckboxBranching(PloneSurveyTestCase):
    """Test sub survey Branching for checkbox questions"""

    def afterSetUp(self):
        """Create a survey with four pages"""
        self.createBranchingSurvey()
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
        next_page = self.ss1.getNextPage()
        assert not self.ss2.displaySubSurvey()
        #assert self.ss3.displaySubSurvey()
        #assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss3/" />' in next_page

    def testAnswerList(self):
        """ss1 with yes should return ss1"""
        self.ss1.ssq2.addAnswer(['Yes', 'No'])
        next_page = self.ss1.getNextPage()
        #assert self.ss3.displaySubSurvey()
        #assert '<base href="http://nohost/plone/Members/test_user_1_/s1/ss3/" />' in next_page, next_page[next_page.find('<base href'):next_page.find('<base href')+100]

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBranchingConditions))
    suite.addTest(makeSuite(TestRadioBranching))
    suite.addTest(makeSuite(TestSubSurveyRadioBranching))
    suite.addTest(makeSuite(TestCheckboxBranching))
    suite.addTest(makeSuite(TestSubSurveyCheckboxBranching))
    return suite
