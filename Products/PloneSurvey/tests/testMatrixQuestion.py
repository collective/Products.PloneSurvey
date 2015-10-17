import unittest

from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent

from plone.app.testing import TEST_USER_ID, setRoles
from Products.Archetypes.utils import DisplayList
from Products.CMFFormController.ControllerState import ControllerState

from base import INTEGRATION_TESTING


class testMatrixQuestion(unittest.TestCase):
    """Ensure survey question can be answered"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
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
                assert question.getAnswerFor(userid) == 'Yes', \
                    "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 2)
        self.assertEqual(answers['smq1'], 'Yes')

    def testLikertOptions(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        smq1.setLikertOptions(1)
        # add your form variables
        self.layer['request'].form['sm1-smq1'] = '1'
        # set up a dummy state object
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=s1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        # get the form controller
        controller = self.portal.portal_form_controller
        # send the validate script to the form controller
        # with the dummy state object
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_survey', ]
        )
        # Do any relevant tests
        assert controller_state.getErrors() == {}, \
            "Validation error raised: %s" % controller_state.getErrors()
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getAllQuestions()
        for question in questions:
            if question.portal_type == 'Survey Matrix Question':
                assert question.getAnswerFor(userid) in \
                    question.getQuestionOptions(), \
                    "Answer not in question options"

    def testCantAddSpam(self):
        s1 = getattr(self, 's1')
        self.layer['request'].form['smq1'] = 'Spam Answer'
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=s1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_survey', ]
        )
        assert controller_state.getErrors() != {}, \
            "Validation error not raised"

    def testCantAddSpamToLikert(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        smq1.setLikertOptions(1)
        self.layer['request'].form['smq1'] = '99'
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=s1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_survey', ]
        )
        assert controller_state.getErrors() != {}, \
            "Validation error not raised"

    def testCantAddTextToLikert(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        smq1.setLikertOptions(1)
        self.layer['request'].form['smq1'] = 'Spam Answer'
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=s1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_survey', ]
        )
        assert controller_state.getErrors() != {}, \
            "Validation error not raised"


class TestRequired(unittest.TestCase):
    """Ensure required field works correctly"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')

    def testSurveyMatrix(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        assert sm1.getRequired() == 1, "Matrix default should be required"
        sm1.setNullValue('Not applicable')
        assert sm1.getRequired() == 0, \
            "Should be required when nullValue exists"

    def testSurveyMatrixQuestion(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        assert smq1.getRequired() == 1, \
            "Matrix Question default should be required"
        sm1.setNullValue('Not applicable')
        assert smq1.getRequired() == 0, \
            "Should be required when nullValue exists"


class TestAnswerOptions(unittest.TestCase):
    """Ensure matrix options are correct"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')

    def testMatrixQuestionOptions(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        assert smq1.getQuestionOptions() == sm1.getAnswerOptions(), \
            "Options not returned correctly"
        sm1.setLikertOptions('1')
        assert isinstance(smq1.getQuestionOptions(), DisplayList), \
            "Likert options not returned correctly"
        options = smq1.getQuestionOptions()
        assert options[0] == 5, "Key of likert option wrong"
        assert options.getValue(5) == 'Very Good', \
            "Value of likert option wrong"
        assert len(smq1.getQuestionOptions()) == 5, \
            "Wrong number of likert options returned"
        smq1.setNullValue('Not applicable')
        assert len(smq1.getQuestionOptions()) == 6, \
            "Wrong number of likert options returned"
        assert smq1.getQuestionOptions().getValue(0) == 'Not applicable', \
            "Null option not first"


class testMatrixQuestionValidation(unittest.TestCase):
    """Ensure survey matrix validates correctly"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        sm1 = getattr(self.s1, 'sm1')
        sm1.setInputType('checkbox')
        sm1.invokeFactory('Survey Matrix Question', 'smq1')
        notify(ObjectCreatedEvent(sm1.smq1))

    def testMultipleCheckboxAnswersValidates(self):
        s1 = getattr(self, 's1')
        # add your form variables
        self.layer['request'].form['sm1-smq1'] = ['5', '4']
        # set up a dummy state object
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=s1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        # get the form controller
        controller = self.portal.portal_form_controller
        # send the validate script to the form controller
        # with the dummy state object
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_survey', ]
        )
        # Do any relevant tests
        assert controller_state.getErrors() == {}, controller_state.getErrors()
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getAllQuestions()
        for question in questions:
            if question.portal_type == 'Survey Matrix Question':
                answer = question.getAnswerFor(userid)
                assert answer == [5, 4], \
                    "Answer not in question options: %s" % answer

    def testMultipleSelectionsAnswersValidates(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        sm1.setInputType("multipleSelect")
        # add your form variables
        self.layer['request'].form['sm1-smq1'] = ['5', '4']
        # set up a dummy state object
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=s1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        # get the form controller
        controller = self.portal.portal_form_controller
        # send the validate script to the form controller
        # with the dummy state object
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_survey', ]
        )
        # Do any relevant tests
        assert controller_state.getErrors() == {}, controller_state.getErrors()
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getAllQuestions()
        for question in questions:
            if question.portal_type == 'Survey Matrix Question':
                answer = question.getAnswerFor(userid)
                assert answer == [5, 4], \
                    "Answer not in question options: %s" % answer
