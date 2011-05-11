#
# Test PloneSurvey interfaces
#
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from Products.PloneSurvey.content.Survey import Survey
from Products.PloneSurvey.content.SurveyMatrixQuestion import SurveyMatrixQuestion
from Products.PloneSurvey.content.SurveySelectQuestion import SurveySelectQuestion
from Products.PloneSurvey.content.SurveyTextQuestion import SurveyTextQuestion
from Products.PloneSurvey.interfaces import *

from base import PloneSurveyTestCase

class TestInterfaces(PloneSurveyTestCase):
    """Ensure survey interfaces are working"""

    def testSurveyImplements(self):
        assert verifyClass(ISurvey, Survey)

    def testSurveyIsAdapted(self):
        assert ISurvey.implementedBy(Survey)

    def testSurveyTextQuestion(self):
        assert verifyClass(ISurveyTextQuestion, SurveyTextQuestion)
        assert ISurveyTextQuestion.implementedBy(SurveyTextQuestion)

    def testPloneSurveyQuestion(self):
        assert verifyClass(IPloneSurveyQuestion, SurveyMatrixQuestion)
        assert IPloneSurveyQuestion.implementedBy(SurveyMatrixQuestion)
        assert verifyClass(IPloneSurveyQuestion, SurveySelectQuestion)
        assert IPloneSurveyQuestion.implementedBy(SurveySelectQuestion)
        assert verifyClass(IPloneSurveyQuestion, SurveyTextQuestion)
        assert IPloneSurveyQuestion.implementedBy(SurveyTextQuestion)

class TestClassesImplements(PloneSurveyTestCase):
    """Ensure survey objects implement the interfaces"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')

    def testSurveyInterface(self):
        from Products.PloneSurvey.interfaces import ISurvey
        SurveyObject = getattr(self.folder, 's1')
        assert ISurvey.providedBy(SurveyObject)
        assert verifyObject(ISurvey, SurveyObject)

    def testSurveyTextQuestionInterface(self):
        from Products.PloneSurvey.interfaces import ISurveyTextQuestion
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')
        assert ISurveyTextQuestion.providedBy(stq1)
        assert verifyObject(ISurveyTextQuestion, stq1)

