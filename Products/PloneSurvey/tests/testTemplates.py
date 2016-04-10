import unittest

from ZPublisher.BaseRequest import BaseRequest as Request

from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.testing import logout

from base import INTEGRATION_TESTING
from base import INTEGRATION_ANON_SURVEY_TESTING
from base import INTEGRATION_BRANCHING_TESTING


class TestTemplatesWork(unittest.TestCase):
    """Ensure templates work correctly"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        self.layer['request'].set('ACTUAL_URL', self.s1.absolute_url())

    def testSurveyView(self):
        """Ensure survey view works"""
        s1 = getattr(self.portal, 's1')
        result = s1.survey_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)

    def testRespondentsView(self):
        """Ensure template does not raise an error with a respondent"""
        s1 = getattr(self.portal, 's1')
        questions = s1.getQuestions()
        for question in questions:
            question.addAnswer('Answer')
        s1.getSurveyId()
        result = s1.respondents_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)


class TestSubSurveyView(unittest.TestCase):
    """Ensure survey view works with multipe value matrix question"""
    layer = INTEGRATION_BRANCHING_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.layer['request'].set('ACTUAL_URL', self.portal.s1.absolute_url())

    def testSurveyView(self):
        """Ensure survey view works for sub survey"""
        s1 = getattr(self.portal, 's1')
        result = s1.ss1.survey_view(REQUEST=Request())
        # XXX this should test that page is redirected to first page
        self.assertEqual(result.find('Error Type') >= 0, False)


class TestSurveyViewWithMultipleMatrix(unittest.TestCase):
    """Ensure survey view works with multipe value matrix question"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')
        self.s1.sm1.smq1.setInputType('multipleSelect')
        self.layer['request'].set('ACTUAL_URL', self.s1.absolute_url())

    def testSurveyView(self):
        """Ensure survey view works"""
        s1 = getattr(self.portal, 's1')
        result = s1.survey_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)


class TestAnonSurveyView(unittest.TestCase):
    """Ensure anonoymous can see the survey"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def testSurveyView(self):
        """Ensure survey view works"""
        logout()
        s1 = getattr(self.portal, 's1')
        result = s1.survey_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)


class TestJavascript(unittest.TestCase):
    """Ensure javascript in relevant templates"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')

    def testJsInSurveyView(self):
        """Ensure reset js in survey view"""
        s1 = getattr(self.portal, 's1')
        result = s1.survey_view(REQUEST=Request())
        assert '++resource++Products.PloneSurvey.javascripts/survey_reset.js' \
            in result

    def testJsInSurveyReset(self):
        """Ensure reset js in reset view"""
        s1 = getattr(self.portal, 's1')
        result = s1.survey_reset_form(REQUEST=Request())
        assert '++resource++Products.PloneSurvey.javascripts/survey_reset.js' \
            in result

    def testJsForDateQuestion(self):
        """Ensure js for date questions"""
        s1 = getattr(self.portal, 's1')
        s1.invokeFactory('Survey Date Question', 'sdq1')
        result = s1.survey_view(REQUEST=Request())
        assert 'jscalendar/calendar_stripped.js' in result
        assert 'jscalendar/calendar-en.js' in result


class TestCss(unittest.TestCase):
    """Ensure css in relevant templates"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')

    def testCssInSurveyBarchart(self):
        """Ensure css in survey barchart"""
        s1 = getattr(self.portal, 's1')
        view = s1.restrictedTraverse('@@Products.PloneSurvey.survey_barchart')
        result = view()
        s = '++resource++Products.PloneSurvey.stylesheets/survey_results.css'
        assert s in result
