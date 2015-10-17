import unittest

from ZPublisher.BaseRequest import BaseRequest as Request

from plone.app.testing import TEST_USER_ID, setRoles

from base import INTEGRATION_TESTING


class testRespondentsCreated(unittest.TestCase):
    """Ensure respondents details correctly converted"""
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
        result = s1.respondents_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)
