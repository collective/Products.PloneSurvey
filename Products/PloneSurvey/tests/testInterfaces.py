#
# Test PloneSurvey interfaces
#

import os, sys
from Interface.Verify import verifyClass
from Testing.makerequest import makerequest

from base import PloneSurveyTestCase

class TestInterfaces(PloneSurveyTestCase):
    """Ensure survey interfaces are working"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')

    def testSurveyInterface(self):
        from Products.PloneSurvey.interfaces import ISurvey
        SurveyObject = getattr(self.folder, 's1')
        ISurvey.providedBy(SurveyObject)
        #verifyClass(ISurvey, SurveyObject)

    def testSurveyTextQuestionInterface(self):
        from Products.PloneSurvey.interfaces import ISurveyTextQuestion
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')
        ISurveyTextQuestion.providedBy(stq1)
        #verifyClass(ISurveyTextQuestion, stq1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInterfaces))
    return suite
