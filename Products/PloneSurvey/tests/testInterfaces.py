#
# Test PloneSurvey interfaces
#
from zope.interface.verify import verifyClass

from Products.PloneSurvey.content.Survey import Survey
from Products.PloneSurvey.content.SurveyMatrixQuestion import SurveyMatrixQuestion
from Products.PloneSurvey.content.SurveySelectQuestion import SurveySelectQuestion
from Products.PloneSurvey.content.SurveyTextQuestion import SurveyTextQuestion
from Products.PloneSurvey.interfaces import *

from base import PloneSurveyTestCase

class TestInterfaces(PloneSurveyTestCase):
    """Ensure survey interfaces are working"""

    def testSurveyImplements(self):
        verifyClass(ISurvey, Survey)

    def testSurveyIsAdapted(self):
        ISurvey.providedBy(Survey)

    def testSurveyTextQuestion(self):
        verifyClass(ISurveyTextQuestion, SurveyTextQuestion)
        ISurveyTextQuestion.providedBy(SurveyTextQuestion)

    def testPloneSurveyQuestion(self):
        verifyClass(IPloneSurveyQuestion, SurveyMatrixQuestion)
        IPloneSurveyQuestion.providedBy(SurveyMatrixQuestion)
        verifyClass(IPloneSurveyQuestion, SurveySelectQuestion)
        IPloneSurveyQuestion.providedBy(SurveySelectQuestion)
        verifyClass(IPloneSurveyQuestion, SurveyTextQuestion)
        IPloneSurveyQuestion.providedBy(SurveyTextQuestion)

class TestClassesImplements(PloneSurveyTestCase):
    """Ensure survey objects implement the interfaces"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')

    def testSurveyInterface(self):
        from Products.PloneSurvey.interfaces import ISurvey
        SurveyObject = getattr(self.folder, 's1')
        ISurvey.providedBy(SurveyObject)
        verifyClass(ISurvey, SurveyObject)

    def testSurveyTextQuestionInterface(self):
        from Products.PloneSurvey.interfaces import ISurveyTextQuestion
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')
        ISurveyTextQuestion.providedBy(stq1)
        verifyClass(ISurveyTextQuestion, stq1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInterfaces))
    return suite
