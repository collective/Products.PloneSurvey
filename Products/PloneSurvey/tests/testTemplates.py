#
# Test PloneSurvey templates
#
from ZPublisher.BaseRequest import BaseRequest as Request

from base import PloneSurveyTestCase

class TestTemplatesWork(PloneSurveyTestCase):
    """Ensure templates work correctly"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Text Question', 'stq1')

    def testSurveyView(self):
        """Ensure survey view works"""
        s1 = getattr(self.folder, 's1')
        result = s1.survey_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)

    def testRespondentsView(self):
        """Ensure template does not raise an error with a respondent"""
        s1 = getattr(self.folder, 's1')
        questions = s1.getQuestions()
        for question in questions:
            question.addAnswer('Answer')
        s1.getSurveyId()
        result = s1.respondents_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)

class TestSubSurveyView(PloneSurveyTestCase):
    """Ensure survey view works with multipe value matrix question"""

    def afterSetUp(self):
        self.createSimpleTwoPageSurvey()

    def testSurveyView(self):
        """Ensure survey view works for sub survey"""
        s1 = getattr(self.folder, 's1')
        result = s1.ss1.survey_view(REQUEST=Request())
        # XXX this should test that page is redirected to first page
        self.assertEqual(result.find('Error Type') >= 0, False)

class TestSurveyViewWithMultipleMatrix(PloneSurveyTestCase):
    """Ensure survey view works with multipe value matrix question"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')
        self.s1.sm1.smq1.setInputType('multipleSelect')

    def testSurveyView(self):
        """Ensure survey view works"""
        s1 = getattr(self.folder, 's1')
        result = s1.survey_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)

class TestAnonSurveyView(PloneSurveyTestCase):
    """Ensure anonoymous can see the survey"""

    def afterSetUp(self):
        self.createAnonSurvey()

    def testSurveyView(self):
        """Ensure survey view works"""
        self.logout()
        s1 = getattr(self.folder, 's1')
        result = s1.survey_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTemplatesWork))
    suite.addTest(makeSuite(TestSubSurveyView))
    suite.addTest(makeSuite(TestSurveyViewWithMultipleMatrix))
    suite.addTest(makeSuite(TestSurveyViewWithMultipleMatrix))
    return suite
