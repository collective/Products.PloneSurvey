#
# Test PloneSurvey Matrix Question
#

import os, sys
from AccessControl import Unauthorized

from Testing.makerequest import makerequest
from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from base import PloneSurveyTestCase

class testMatrixQuestion(PloneSurveyTestCase):
    """Ensure survey question can be answered"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')

    def testAddAnswer(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getAllQuestions()
        self.assertEqual(len(questions), 1)
        for question in questions:
            if question.portal_type == 'Survey Matrix Question':
                question.addAnswer('Yes')
                assert question.getAnswerFor(userid) == 'Yes', "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 2)
        self.assertEqual(answers['smq1'], 'Yes')

    def testLikertOptions(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        smq1.setLikertOptions(1)
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['sm1-smq1'] = '1'
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
        assert controller_state.getErrors() == {}, "Validation error raised: %s" % controller_state.getErrors()
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getAllQuestions()
        for question in questions:
            if question.portal_type == 'Survey Matrix Question':
                assert question.getAnswerFor(userid) in question.getQuestionOptions(), "Answer not in question options"

    def testCantAddSpam(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        app = makerequest(self.app)
        app.REQUEST.form['smq1'] = 'Spam Answer'
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
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        smq1.setLikertOptions(1)
        app = makerequest(self.app)
        app.REQUEST.form['smq1'] = '99'
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
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        smq1.setLikertOptions(1)
        app = makerequest(self.app)
        app.REQUEST.form['smq1'] = 'Spam Answer'
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

class testMatrixQuestionValidation(PloneSurveyTestCase):
    """Ensure survey matrix validates correctly"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        sm1 = getattr(self.s1, 'sm1')
        sm1.setInputType('checkbox')
        sm1.invokeFactory('Survey Matrix Question', 'smq1')

    def testMultipleCheckboxAnswersValidates(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')        
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['sm1-smq1'] = ['5', '4']
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
        assert controller_state.getErrors() == {}, controller_state.getErrors()
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getAllQuestions()
        for question in questions:
            if question.portal_type == 'Survey Matrix Question':
                answer = question.getAnswerFor(userid)
                assert answer == [5, 4], "Answer not in question options: %s" % answers

    def testMultipleSelectionsAnswersValidates(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        sm1.setInputType("multipleSelect")
        smq1 = getattr(sm1, 'smq1')
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['sm1-smq1'] = ['5', '4']
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
        assert controller_state.getErrors() == {}, controller_state.getErrors()
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getAllQuestions()
        for question in questions:
            if question.portal_type == 'Survey Matrix Question':
                answer = question.getAnswerFor(userid)
                assert answer == [5, 4], "Answer not in question options: %s" % answers

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMatrixQuestion))
    suite.addTest(makeSuite(testMatrixQuestionValidation))
    return suite
