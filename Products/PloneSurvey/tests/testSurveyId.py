#
# Test PloneSurvey Survey ID
#
from DateTime import DateTime
from Testing.makerequest import makerequest

from Products.CMFFormController.ControllerState import ControllerState

from base import PloneSurveyTestCase

class TestSurveyId(PloneSurveyTestCase):
    """Ensure surveyId method returns right thing"""

    def afterSetUp(self):
        self.createAnonSurvey()

    def testSurveyId(self):
        """test for test user"""
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == 'test_user_1_'

    def testIdForOtherUser(self):
        """test for another user"""
        self.addMember('a_user', 'A User', 'user@here.com', '(Member,)', DateTime())
        self.logout()
        self.login('a_user')
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == 'a_user'

class TestAnonymousId(PloneSurveyTestCase):
    """Ensure anonymous id is correctly constructed"""

    def afterSetUp(self):
        self.createSubSurvey()

    def testAnonymousIdGeneration(self):
        s1 = getattr(self, 's1')
        now = DateTime()
        self.logout()
        userid = s1.getSurveyId()
        expected_userid = 'Anonymous' + '@' + str(now)
        assert userid[:-9] == expected_userid[:-9], "Anonymous id generation not working - %s" % userid

class TestNoCookiesWorks(PloneSurveyTestCase):
    """Ensure survey can be answered with no cookies enabled"""

    def afterSetUp(self):
        self.createSimpleTwoPageSurvey()
        self.logout()

    def testCanAnswerFirstPage(self):
        s1 = getattr(self, 's1')
        app = makerequest(self.app)
        app.REQUEST.form['stq1'] = 'An answer'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert controller_state.getErrors() == {}, "Validation error raised"

    def testSecondPageRedirects(self):
        s1 = getattr(self, 's1')
        app = makerequest(self.app)
        app.REQUEST.form['stq2'] = 'Another answer'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1.ss1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert controller_state.getErrors() == {}, "Validation error raised"

    def testTwoRequests(self):
        s1 = getattr(self, 's1')
        survey_id = s1.getSurveyId()
        app = makerequest(self.app)
        app.REQUEST.form['stq1'] = 'An answer'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert controller_state.getErrors() == {}, "Validation error raised"
        app = makerequest(self.app)
        app.REQUEST.form['stq2'] = 'Another answer'
        app.REQUEST.form['survey_user_id'] = s1.getRespondents()[0]
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1.ss1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert controller_state.getErrors() == {}, "Validation error raised"
        respondents = s1.getRespondents()
        assert len(respondents) == 1, respondents

class TestReturnsFirstPage(PloneSurveyTestCase):
    """Ensure survey returns first page, if no survey ID exists in request"""

    def afterSetUp(self):
        self.createSubSurvey()

    def testAnonymousIdGeneration(self):
        s1 = getattr(self, 's1')
        now = DateTime()
        self.logout()
        userid = s1.getSurveyId()
        expected_userid = 'Anonymous' + '@' + str(now)
        assert userid[:-9] == expected_userid[:-9], "Anonymous id generation not working - %s" % userid

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSurveyId))
    suite.addTest(makeSuite(TestAnonymousId))
    suite.addTest(makeSuite(TestNoCookiesWorks))
    suite.addTest(makeSuite(TestReturnsFirstPage))
    return suite
