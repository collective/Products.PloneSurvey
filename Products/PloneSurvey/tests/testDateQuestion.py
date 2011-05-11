#
# Test PloneSurvey Date Question
#
from DateTime.DateTime import DateTime
from Testing.makerequest import makerequest

from Products.Archetypes.utils import DisplayList
from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from base import PloneSurveyTestCase

class testAddDateQuestion(PloneSurveyTestCase):
    """Ensure date question works correctly"""

    def afterSetUp(self):
        self.createAnonSurvey()

    def testCreateDateQuestion(self):
        s1 = getattr(self, 's1')
        s1.invokeFactory('Survey Date Question', 'sdq1')
        assert 'sdq1' in s1.objectIds()

class testPostValidate(PloneSurveyTestCase):
    """Ensure post validation works correctly"""

    def afterSetUp(self):
        self.createAnonSurvey()
        self.s1.invokeFactory('Survey Date Question', 'sdq1')
        self.app = makerequest(self.app)
        self.app.REQUEST.form['title'] = 'Date Question Title'
        self.app.REQUEST.form['showYMD'] = True
        self.app.REQUEST.form['showHM'] = True
        self.app.REQUEST.form['startingYear'] = '1970'
        self.app.REQUEST.form['endingYear'] = '2001'
        self.app.REQUEST.form['futureYears'] = ''

    def testFormValidates(self):
        """Test form validates correctly"""
        sdq1 = getattr(self.s1, 'sdq1')
        app = self.app
        dummy_controller_state = ControllerState(
                                    id='base_edit',
                                    context=sdq1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_base',])
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.app.REQUEST, errors)
        assert errors == {}, "Validation error raised: %s" % controller_state.getErrors()

    def testIntegers(self):
        """Test validation fails if an integer field is a string"""
        sdq1 = getattr(self.s1, 'sdq1')
        self.app.REQUEST.form['startingYear'] = 'string'
        self.app.REQUEST.form['endingYear'] = 'string'
        self.app.REQUEST.form['futureYears'] = 'string'
        app = self.app
        dummy_controller_state = ControllerState(
                                    id='base_edit',
                                    context=sdq1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_base',])
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.app.REQUEST, errors)
        assert errors != {}, "Validation error not raised"
        assert errors.has_key('startingYear')
        assert errors.has_key('endingYear')
        assert errors.has_key('futureYears')

    def testQuestionField(self):
        """Test validation fails if ymd and hm both unselected"""
        sdq1 = getattr(self.s1, 'sdq1')
        self.app.REQUEST.form['showYMD'] = False
        self.app.REQUEST.form['showHM'] = False
        app = self.app
        dummy_controller_state = ControllerState(
                                    id='base_edit',
                                    context=sdq1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_base',])
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.app.REQUEST, errors)
        assert errors != {}, "Validation error not raised"
        assert errors.has_key('showYMD')
        assert errors.has_key('showHM')

    def testEndYear(self):
        """Test validation fails if end year is before start year"""
        sdq1 = getattr(self.s1, 'sdq1')
        self.app.REQUEST.form['endingYear'] = '1969'
        app = self.app
        dummy_controller_state = ControllerState(
                                    id='base_edit',
                                    context=sdq1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_base',])
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.app.REQUEST, errors)
        assert errors != {}, "Validation error not raised"
        assert errors.has_key('endingYear')

    def testFutureYear(self):
        """Test validation passes if future year, and no end year"""
        sdq1 = getattr(self.s1, 'sdq1')
        self.app.REQUEST.form['endingYear'] = ''
        self.app.REQUEST.form['futureYears'] = '5'
        app = self.app
        dummy_controller_state = ControllerState(
                                    id='base_edit',
                                    context=sdq1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_base',])
        errors = controller_state.getErrors()
        errors = sdq1.post_validate(self.app.REQUEST, errors)
        assert errors == {}, "Validation error raised: %s" % errors

class testDateQuestion(PloneSurveyTestCase):
    """Ensure date question works correctly"""

    def afterSetUp(self):
        self.createAnonSurvey()
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
                assert question.getAnswerFor(userid) == now, "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)

    def testValidationRequiredSplitDate(self):
        s1 = getattr(self, 's1')
        sdq1 = getattr(s1, 'sdq1')
        sdq1.setRequired(True)
        app = makerequest(self.app)
        now = DateTime()
        now_value = str(now.year()) + '/' + str(now.month()) + '/' + str(now.day()) + ' ' + str(now.hour()) + ':' + str(now.minute()) + ':00 GMT'
        self.app.REQUEST.form['sdq1_ampm'] = ''
        self.app.REQUEST.form['sdq1_day'] = str(now.day())
        self.app.REQUEST.form['sdq1_hour'] = str(now.hour())
        self.app.REQUEST.form['sdq1_minute'] = str(now.minute())
        self.app.REQUEST.form['sdq1_month'] = str(now.month())
        self.app.REQUEST.form['sdq1_year'] = str(now.year())
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert controller_state.getErrors() == {}, "Validation error raised: %s" % controller_state.getErrors()
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Date Question':
                assert question.getAnswerFor(userid) == now_value, "Answer not saved correctly: %s" % question.getAnswerFor(userid)

