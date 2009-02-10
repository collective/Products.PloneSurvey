#
# Test PloneSurvey backward compatibility
#

#import os, sys
#from DateTime import DateTime
from ZPublisher.BaseRequest import BaseRequest as Request

#from Products.CMFCore.utils import getToolByName

#from Products.PloneSurvey import permissions
from base import PloneSurveyTestCase

class testRespondentsCreated(PloneSurveyTestCase):
    """Ensure respondents details correctly converted"""

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
        userid = s1.getSurveyId()
        questions = s1.getQuestions()
        for question in questions:
            question.addAnswer('Answer')
        result = s1.respondents_view(REQUEST=Request())
        self.assertEqual(result.find('Error Type') >= 0, False)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testRespondentsCreated))
    return suite
