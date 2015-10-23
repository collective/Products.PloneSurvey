import unittest

from plone.app.testing import TEST_USER_ID, setRoles

from Products.CMFFormController.ControllerState import ControllerState

from base import INTEGRATION_TESTING


class testTextValidation(unittest.TestCase):
    """Test survey text question validation"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Text Question', 'stq1')

    def testAddAnswer(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Yes')
                assert question.getAnswerFor(userid) == 'Yes', \
                    "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)

    def testValidateScript(self):
        s1 = getattr(self, 's1')
        self.layer['request'].form['stq1'] = 'Text Answer'
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
        assert controller_state.getErrors() == {}, "Validation error raised"


class TestLengthValidation(unittest.TestCase):
    """Ensure validation for text length"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')
        stq1.setRequired(True)
        stq1.setValidation('None')

    def testQuestionValidates(self):
        s1 = getattr(self, 's1')
        # add your form variables
        self.layer['request'].form['stq1'] = 'Text Answer'
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
        assert controller_state.getErrors() == {}, "Validation error raised"
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Text answer')
                assert question.getAnswerFor(userid) == 'Text answer', \
                    "Answer not saved correctly"

    def testValidateLengthPasses(self):
        s1 = getattr(self, 's1')
        stq1 = getattr(self.s1, 'stq1')
        stq1.setMaxLength(50)
        # add your form variables
        self.layer['request'].form['stq1'] = 'Text Answer'
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
            "Validation error not raised"

    def testValidateLengthFails(self):
        s1 = getattr(self, 's1')
        stq1 = getattr(self.s1, 'stq1')
        stq1.setMaxLength(5)
        # add your form variables
        self.layer['request'].form['stq1'] = 'Text Answer'
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
        assert controller_state.getErrors() != {}, \
            "Validation error not raised"


class TestEmailValidation(unittest.TestCase):
    """Test email validation on a text question"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        self.s1.stq1.setValidation('isEmail')

    def testEmailValidationPasses(self):
        s1 = getattr(self, 's1')
        self.layer['request'].form['stq1'] = 'someone@somewhere.com'
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
        assert controller_state.getErrors() == {}, \
            "Validation error raised"

    def testEmailValidationFails(self):
        s1 = getattr(self, 's1')
        self.layer['request'].form['stq1'] = 'Not an email address'
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
            self.layer['request'], ['validate_survey', ]
        )
        assert controller_state.getErrors() != {}, \
            "Validation error not raised"
