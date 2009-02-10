#
# Test PloneSurvey Select Question
#

import os, sys
from AccessControl import Unauthorized

from Testing.makerequest import makerequest
from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from base import PloneSurveyTestCase

class testSelectQuestion(PloneSurveyTestCase):
    """Ensure survey question can be answered"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testAddAnswer(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Select Question':
                question.addAnswer('Yes')
                assert question.getAnswerFor(userid) == 'Yes', "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)

    def testLikertOptions(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setLikertOptions(1)
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['ssq1'] = '1'
        # set up a dummy state object
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        # get the form controller
        controller = self.portal.portal_form_controller
        # send the validate script to the form controller with the dummy state object
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        # Do any relevant tests
        assert controller_state.getErrors() == {}, "Validation error raised"
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Select Question':
                assert question.getAnswerFor(userid) in question.getQuestionOptions(), "Answer not in question options"

    def testCantAddSpam(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        app = makerequest(self.app)
        app.REQUEST.form['ssq1'] = 'Spam Answer'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert controller_state.getErrors() != {}, "Validation error not raised"

    def testCantAddSpamToLikert(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setLikertOptions(1)
        app = makerequest(self.app)
        app.REQUEST.form['ssq1'] = '99'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert controller_state.getErrors() != {}, "Validation error not raised"

    def testCantAddTextToLikert(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setLikertOptions(1)
        app = makerequest(self.app)
        app.REQUEST.form['ssq1'] = 'Spam Answer'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert controller_state.getErrors() != {}, "Validation error not raised"

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSelectQuestion))
    return suite
