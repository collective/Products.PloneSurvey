import transaction
import unittest

from DateTime import DateTime

from plone.app.testing import login, logout
from plone.app.testing import TEST_USER_ID, setRoles
from ZPublisher.BaseRequest import BaseRequest as Request


from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from base import INTEGRATION_ANON_SURVEY_TESTING


class TestSurveyId(unittest.TestCase):
    """Ensure surveyId method returns right thing"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def testSurveyId(self):
        """test for test user"""
        s1 = getattr(self.portal, 's1')
        userid = s1.getSurveyId()
        assert userid == 'test_user_1_'

    def testIdForOtherUser(self):
        """test for another user"""
        self.portal_membership = getToolByName(self.portal,
                                               'portal_membership')
        self.portal_membership.addMember(
            'a_user',
            'secret',
            ['Member', ],
            [],
            {'fullname': 'A User', 'email': 'user@here.com', }
        )
        logout()
        login(self.portal, 'a_user')
        s1 = getattr(self.portal, 's1')
        userid = s1.getSurveyId()
        assert userid == 'a_user'


class TestAnonymousId(unittest.TestCase):
    """Ensure anonymous id is correctly constructed"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        s1 = getattr(self.portal, 's1')
        s1.invokeFactory('Sub Survey', 'ss1')

    def testAnonymousIdGeneration(self):
        s1 = getattr(self.portal, 's1')
        now = DateTime()
        logout()
        userid = s1.getSurveyId()
        expected_userid = 'Anonymous' + '@' + str(now)
        assert userid[:-12] == expected_userid[:-12], \
            "Anonymous id generation not working - %s, %s" % (userid,
                                                              expected_userid)


class TestNoCookiesWorks(unittest.TestCase):
    """Ensure survey can be answered with no cookies enabled"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        s1 = getattr(self.portal, 's1')
        s1.invokeFactory('Sub Survey', 'ss1')
        s1.invokeFactory('Survey Text Question', 'stq1')
        s1.ss1.invokeFactory('Survey Text Question', 'stq2')
        logout()

    def testCanAnswerFirstPage(self):
        s1 = getattr(self.portal, 's1')
        self.layer['request'].form['stq1'] = 'An answer'
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
        assert controller_state.getErrors() == {}, controller_state.getErrors()

    def testSecondPageRedirects(self):
        s1 = getattr(self.portal, 's1')
        self.layer['request'].form['stq2'] = 'Another answer'
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=s1.ss1,
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
        assert controller_state.getErrors() == {}, controller_state.getErrors()

    def testTwoRequests(self):
        s1 = getattr(self.portal, 's1')
        self.layer['request'].form['stq1'] = 'An answer'
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
        assert controller_state.getErrors() == {}, controller_state.getErrors()
        self.layer['request'].form['stq2'] = 'Another answer'
        self.layer['request'].form['survey_user_id'] = \
            s1.getRespondentsList()[0]
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=s1.ss1,
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
        assert controller_state.getErrors() == {}, controller_state.getErrors()
        respondents = s1.getRespondentsList()
        assert len(respondents) == 1, respondents


class TestReturnsFirstPage(unittest.TestCase):
    """Ensure survey returns first page, if no survey ID exists in request"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        s1 = getattr(self.portal, 's1')
        s1.invokeFactory('Sub Survey', 'ss1')

    def testAnonymousIdGeneration(self):
        s1 = getattr(self.portal, 's1')
        now = DateTime()
        logout()
        userid = s1.getSurveyId()
        expected_userid = 'Anonymous' + '@' + str(now)
        assert userid[:-12] == expected_userid[:-12], \
            "Anonymous id generation not working - %s, %s" % (userid,
                                                              expected_userid)


class TestReadDoesNotWrite(unittest.TestCase):
    """Ensure survey does not commit on first read"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.s1 = getattr(self.portal, 's1')
        s1 = getattr(self.portal, 's1')
        s1.invokeFactory('Survey Text Question', 'stq1')

    def testReadDoesNotWrite(self):
        s1 = getattr(self.portal, 's1')
        # commit, as we've added a question
        transaction.commit()
        original_size = s1._p_estimated_size
        respondent_size = s1.respondents._p_estimated_size
        assert s1.getRespondentsList() == []
        logout()
        assert s1._p_changed is False
        assert s1.respondents._p_changed is False
        assert s1.stq1._p_changed is False
        # view the survey
        result = s1.survey_view(REQUEST=Request())
        assert s1._p_changed is False
        assert s1.respondents._p_changed is False
        assert s1.stq1._p_changed is False
        transaction.commit()
        # XXX this should not cause an increase in the object size
        assert s1._p_estimated_size == original_size, \
            "Survey size increased from %s to %s" % (original_size,
                                                     s1._p_estimated_size)
        # submit a response
        self.layer['request'].form['stq1'] = 'An answer'
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
        assert controller_state.getErrors() == {}, controller_state.getErrors()
        assert len(s1.getRespondentsList()) == 1
        assert s1._p_changed is False
        assert s1.respondents._p_changed is True
        assert s1.stq1._p_changed is False
        transaction.commit()
        # the survey itself should not increase in size
        assert s1._p_estimated_size == original_size, \
            "Survey size increased from %s to %s" % (original_size,
                                                     s1._p_estimated_size)
        # the respondents should increase in size
        assert s1.respondents._p_estimated_size > respondent_size, \
            "Respondents size increased from %s to %s" % (
                respondent_size,
                s1.respondents._p_estimated_size)
