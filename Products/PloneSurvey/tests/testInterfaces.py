import unittest

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from plone.app.testing import TEST_USER_ID, setRoles

from Products.PloneSurvey.content.Survey import Survey
from Products.PloneSurvey.content.SurveyMatrixQuestion \
    import SurveyMatrixQuestion
from Products.PloneSurvey.content.SurveySelectQuestion \
    import SurveySelectQuestion
from Products.PloneSurvey.content.SurveyTextQuestion \
    import SurveyTextQuestion
from Products.PloneSurvey.interfaces.survey_question \
    import IPloneSurveyQuestion
from Products.PloneSurvey.interfaces.survey import ISurvey
from Products.PloneSurvey.interfaces.survey_text_question \
    import ISurveyTextQuestion

from base import INTEGRATION_TESTING


class TestInterfaces(unittest.TestCase):
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


class TestClassesImplements(unittest.TestCase):
    """Ensure survey objects implement the interfaces"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')

    def testSurveyInterface(self):
        SurveyObject = getattr(self.portal, 's1')
        assert ISurvey.providedBy(SurveyObject)
        assert verifyObject(ISurvey, SurveyObject)

    def testSurveyTextQuestionInterface(self):
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')
        assert ISurveyTextQuestion.providedBy(stq1)
        assert verifyObject(ISurveyTextQuestion, stq1)
