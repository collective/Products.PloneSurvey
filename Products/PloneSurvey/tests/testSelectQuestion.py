#
# Test PloneSurvey Select Question
#
from Testing.makerequest import makerequest

from Products.Archetypes.utils import DisplayList
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

class TestRequired(PloneSurveyTestCase):
    """Ensure required field works correctly"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testSurveySelectQuestion(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        assert ssq1.getRequired() == 1, "Select Question default should be required"
        ssq1.setNullValue('Not applicable')
        assert ssq1.getRequired() == 0, "Should be required when nullValue exists"

class TestAnswerOptions(PloneSurveyTestCase):
    """Ensure select answer options are correct"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testSelectQuestionOptions(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        assert ssq1.getQuestionOptions() == ssq1.getAnswerOptions(), "Options not returned correctly"
        ssq1.setLikertOptions('1')
        assert isinstance(ssq1.getQuestionOptions(), DisplayList), "Likert options not returned correctly"
        options = ssq1.getQuestionOptions()
        assert options[0] == 5, "Key of likert option wrong"
        assert options.getValue(5) == 'Very Good', "Value of likert option wrong"
        assert len(ssq1.getQuestionOptions()) == 5, "Wrong number of likert options returned: %s" % ssq1.getQuestionOptions()
        ssq1.setNullValue('Not applicable')
        assert len(ssq1.getQuestionOptions()) == 6, "Wrong number of likert options returned: %s" % ssq1.getQuestionOptions()
        assert ssq1.getQuestionOptions().getValue(0) == 'Not applicable', "Null option not first"

    def testSelectQuestionOptionsOrderVocabOption1(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setLikertOptions('1')
        ssq1.setReverseLikert(True)
        options = ssq1.getQuestionOptions()
        assert options[0] == 1, "Key of likert option wrong"

    def testSelectQuestionOptionsOrderOption2(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setLikertOptions('2')
        ssq1.setReverseLikert(True)
        options = ssq1.getQuestionOptions()
        assert options[0] == 1, "Key of likert option wrong"

class TestSelectValidation(PloneSurveyTestCase):
    """Ensure survey select validation"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        ssq1 = getattr(self.s1, 'ssq1')
        ssq1.setInputType('checkbox')

    def testMultipleCheckboxAnswersValidates(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['ssq1'] = ['Yes', 'No']
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
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Select Question':
                answer = question.getAnswerFor(userid)
                assert answer == ['Yes', 'No'], "Answer not saved correctly: %s" %answer

    def testMultipleSelectionsAnswersValidates(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setInputType("multipleSelect")
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['ssq1'] = ['Yes', 'No']
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
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Select Question':
                answer = question.getAnswerFor(userid)
                assert answer == ['Yes', 'No'], "Answer not saved correctly: %s" %answer

    def testMultipleLikertValidates(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setLikertOptions(1)
        app = makerequest(self.app)
        # add your form variables
        app.REQUEST.form['ssq1'] = ['1', '2']
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
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Select Question':
                answer = question.getAnswerFor(userid)
                assert answer == [1, 2], "Answer not saved correctly: %s" %answer

class TestSelectComment(PloneSurveyTestCase):
    """Ensure survey validation"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        self.s1.ssq1.setCommentType('text')

    def testAnswerWithComment(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        userid = s1.getSurveyId()
        ssq1.addAnswer('Yes', 'Comment')
        assert ssq1.getAnswerFor(userid) == 'Yes', "Answer not saved correctly"
        assert ssq1.getCommentsFor(userid) == 'Comment', "Comment not saved correctly"

    def testNoAnswerWithComment(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        userid = s1.getSurveyId()
        ssq1.addAnswer('', 'Comment')
        assert ssq1.getAnswerFor(userid) == '', "Answer not saved correctly"
        assert ssq1.getCommentsFor(userid) == 'Comment', "Comment not saved correctly"

    def testValidatesAnswerWithComment(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        userid = s1.getSurveyId()
        app = makerequest(self.app)
        app.REQUEST.form['ssq1'] = 'Yes'
        app.REQUEST.form['ssq1_comments'] = 'Comment'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert ssq1.getAnswerFor(userid) == 'Yes', "Answer not saved correctly"
        assert ssq1.getCommentsFor(userid) == 'Comment', "Comment not saved correctly"

    def testValidatesNoAnswerWithComment(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        userid = s1.getSurveyId()
        app = makerequest(self.app)
        app.REQUEST.form['ssq1'] = ''
        app.REQUEST.form['ssq1_comments'] = 'Comment'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert ssq1.getAnswerFor(userid) == '', "Answer not saved correctly: %s" %ssq1.getAnswerFor(userid)
        assert ssq1.getCommentsFor(userid) == 'Comment', "Comment not saved correctly"

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSelectQuestion))
    suite.addTest(makeSuite(TestRequired))
    suite.addTest(makeSuite(TestAnswerOptions))
    suite.addTest(makeSuite(TestSelectValidation))
    suite.addTest(makeSuite(TestSelectComment))
    return suite
