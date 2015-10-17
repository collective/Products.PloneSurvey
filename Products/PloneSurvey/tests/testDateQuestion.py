import unittest

from DateTime.DateTime import DateTime

from Products.CMFFormController.ControllerState import ControllerState

from base import INTEGRATION_ANON_SURVEY_TESTING


class testAddDateQuestion(unittest.TestCase):
    """Ensure date question works correctly"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def testCreateDateQuestion(self):
        s1 = getattr(self.portal, 's1')
        s1.invokeFactory('Survey Date Question', 'sdq1')
        assert 'sdq1' in s1.objectIds()


class testPostValidate(unittest.TestCase):
    """Ensure post validation works correctly"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Date Question', 'sdq1')
        self.layer['request'].form['title'] = 'Date Question Title'
        self.layer['request'].form['showYMD'] = True
        self.layer['request'].form['showHM'] = True
        self.layer['request'].form['startingYear'] = '1970'
        self.layer['request'].form['endingYear'] = '2001'
        self.layer['request'].form['futureYears'] = ''

    def testFormValidates(self):
        """Test form validates correctly"""
        sdq1 = getattr(self.s1, 'sdq1')
        dummy_controller_state = ControllerState(
            id='base_edit',
            context=sdq1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_base', ]
        )
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.layer['request'], errors)
        assert errors == {}, \
            "Validation error raised: %s" % controller_state.getErrors()

    def testIntegers(self):
        """Test validation fails if an integer field is a string"""
        sdq1 = getattr(self.s1, 'sdq1')
        self.layer['request'].form['startingYear'] = 'string'
        self.layer['request'].form['endingYear'] = 'string'
        self.layer['request'].form['futureYears'] = 'string'
        dummy_controller_state = ControllerState(
            id='base_edit',
            context=sdq1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_base', ]
        )
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.layer['request'], errors)
        assert errors != {}, "Validation error not raised"
        assert 'startingYear' in errors
        assert 'endingYear' in errors
        assert 'futureYears' in errors

    def testQuestionField(self):
        """Test validation fails if ymd and hm both unselected"""
        sdq1 = getattr(self.s1, 'sdq1')
        self.layer['request'].form['showYMD'] = False
        self.layer['request'].form['showHM'] = False
        dummy_controller_state = ControllerState(
            id='base_edit',
            context=sdq1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_base', ]
        )
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.layer['request'], errors)
        assert errors != {}, "Validation error not raised"
        assert 'showYMD' in errors
        assert 'showHM' in errors

    def testEndYear(self):
        """Test validation fails if end year is before start year"""
        sdq1 = getattr(self.s1, 'sdq1')
        self.layer['request'].form['endingYear'] = '1969'
        dummy_controller_state = ControllerState(
            id='base_edit',
            context=sdq1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_base', ]
        )
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.layer['request'], errors)
        assert errors != {}, "Validation error not raised"
        assert 'endingYear' in errors

    def testFutureYear(self):
        """Test validation passes if future year, and no end year"""
        sdq1 = getattr(self.s1, 'sdq1')
        self.layer['request'].form['endingYear'] = ''
        self.layer['request'].form['futureYears'] = '5'
        dummy_controller_state = ControllerState(
            id='base_edit',
            context=sdq1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_base', ]
        )
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.layer['request'], errors)
        assert errors == {}, "Validation error raised: %s" % errors


class testDateQuestion(unittest.TestCase):
    """Ensure date question works correctly"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Date Question', 'sdq1')

    def testAddAnswer(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        now = DateTime()
        for question in questions:
            if question.portal_type == 'Survey Date Question':
                question.addAnswer(now)
                assert question.getAnswerFor(userid) == now, \
                    "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)

    def testValidationRequiredSplitDate(self):
        s1 = getattr(self, 's1')
        sdq1 = getattr(s1, 'sdq1')
        sdq1.setRequired(True)
        now = DateTime()
        now_value = str(now.year()) + \
            '/' + str(now.month()) + \
            '/' + str(now.day()) + \
            ' ' + str(now.hour()) + \
            ':' + str(now.minute()) + \
            ':00 GMT'
        self.layer['request'].form['sdq1_ampm'] = ''
        self.layer['request'].form['sdq1_day'] = str(now.day())
        self.layer['request'].form['sdq1_hour'] = str(now.hour())
        self.layer['request'].form['sdq1_minute'] = str(now.minute())
        self.layer['request'].form['sdq1_month'] = str(now.month())
        self.layer['request'].form['sdq1_year'] = str(now.year())
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
            "Validation error raised: %s" % controller_state.getErrors()
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Date Question':
                assert question.getAnswerFor(userid) == now_value, \
                    "Answer not saved correctly: %s" \
                    % question.getAnswerFor(userid)
