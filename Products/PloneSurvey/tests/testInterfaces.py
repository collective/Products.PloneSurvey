#
# Test PloneSurvey interfaces
#
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from Products.Archetypes.interfaces import IMultiPageSchema

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

class TestMultiPageInterface(PloneSurveyTestCase):
    """Ensure survey objects implement the multi page interface"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')

    def testSurvey(self):
        SurveyObject = self.s1
        assert IMultiPageSchema.providedBy(SurveyObject)

    def testSubSurvey(self):
        """Sub survey doesn't seem to need to be marked with multi page schema"""
        s1 = self.s1
        s1.invokeFactory('Sub Survey', 'ss1')
        SubSurveyObject = getattr(s1, 'ss1')
        assert not IMultiPageSchema.providedBy(SubSurveyObject)

    def testSurveyDateQuestion(self):
        s1 = self.s1
        s1.invokeFactory('Survey Date Question', 'sdq1')
        SurveyDateQuestionObject = getattr(s1, 'sdq1')
        assert IMultiPageSchema.providedBy(SurveyDateQuestionObject)

    def testSurveyMatrix(self):
        s1 = self.s1
        s1.invokeFactory('Survey Matrix', 'sm1')
        SurveyMatrixObject = getattr(s1, 'sm1')
        assert IMultiPageSchema.providedBy(SurveyMatrixObject)

    def testSurveyMatrixQuestion(self):
        s1 = self.s1
        s1.invokeFactory('Survey Matrix', 'sm1')
        s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')
        SurveyMatrixQuestionObject = getattr(s1.sm1, 'smq1')
        assert not IMultiPageSchema.providedBy(SurveyMatrixQuestionObject)

    def testSurveySelectQuestion(self):
        s1 = self.s1
        s1.invokeFactory('Survey Select Question', 'ssq1')
        SurveySelectQuestionObject = getattr(s1, 'ssq1')
        assert IMultiPageSchema.providedBy(SurveySelectQuestionObject)

    def testSurveTextQuestion(self):
        s1 = self.s1
        s1.invokeFactory('Survey Text Question', 'stq1')
        SurveyTextQuestionObject = getattr(s1, 'stq1')
        assert not IMultiPageSchema.providedBy(SurveyTextQuestionObject)
