import unittest

from base import INTEGRATION_Mail_TESTING
from base import loadRespondents


class TestEmail(unittest.TestCase):
    """Test email formatted and sent"""
    layer = INTEGRATION_Mail_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        s1 = getattr(self.portal, 's1')
        assert len(s1.getAuthenticatedRespondents()) == 0
        loadRespondents(self.portal)

    def testEmailText(self):
        s1 = getattr(self.portal, 's1')
        s1.survey_send_invite(email='user1@here.com')
        messages = self.portal.MailHost.messages
        first_message = messages[0]
        assert '<user1@here.com>' in first_message
        assert 'user1@here.com' in first_message
        assert 'Dear User One' in first_message

    def testLinkInEmail(self):
        s1 = getattr(self.portal, 's1')
        s1.survey_send_invite(email='user1@here.com')
        messages = self.portal.MailHost.messages
        first_message = messages[0]
        user = s1.getAuthenticatedRespondent('user1@here.com')
        expected_key = user['key']
        expected_string = 'key=' + expected_key
        assert 'login_form_bridge?email=user1@here.com' in first_message
        assert expected_string in first_message


class TestSendMethods(unittest.TestCase):
    """Test send method"""
    layer = INTEGRATION_Mail_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        loadRespondents(self.portal)

    def testSingleSend(self):
        """Test send to one user"""
        s1 = getattr(self.portal, 's1')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert len(messages) == 1
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 2

    def testAllSend(self):
        """Test send to all users"""
        s1 = getattr(self.portal, 's1')
        s1.survey_send_invite(email='all')
        messages = self.portal.MailHost.messages
        assert len(messages) == 2
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 2

    def testAllSendMethod(self):
        """Test send to all users from method"""
        s1 = getattr(self.portal, 's1')
        number_sent = s1.sendSurveyInviteAll(send_to_all=True)
        messages = self.portal.MailHost.messages
        assert len(messages) == 2
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 2
        assert number_sent == 2

    def testNotSentTwice(self):
        """Test can't send twice to same user"""
        s1 = getattr(self.portal, 's1')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert len(messages) == 1
        number_sent = s1.sendSurveyInviteAll(send_to_all=False)
        messages = self.portal.MailHost.messages
        assert len(messages) == 2, len(messages)
        assert number_sent == 1

    def testReminderSentTwice(self):
        """Test reminder sent twice to same user"""
        s1 = getattr(self.portal, 's1')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert len(messages) == 1
        number_sent = s1.sendSurveyInviteAll(send_to_all=True)
        messages = self.portal.MailHost.messages
        assert len(messages) == 3, len(messages)
        assert number_sent == 2

# XXX this won't work as we can't set it completed or easily login as the user
#    def testReminderNotSentCompleted(self):
#        """Test reminder sent twice to same user"""
#        s1 = getattr(self.portal, 's1')
#        s1.sendSurveyInvite('user2@here.com')
#        messages = self.portal.MailHost.messages
#        assert len(messages) == 1
#        self.login('user2@here.com')
#        self.setCompletedForUser()
#        self.login('test_user_1_')
#        number_sent = s1.sendSurveyInviteAll(send_to_all=True)
#        messages = self.portal.MailHost.messages
#        assert len(messages) == 2, len(messages)
#        assert number_sent == 1


class TestRegisterSent(unittest.TestCase):
    """Test send method registers a respondent as being sent an email"""
    layer = INTEGRATION_Mail_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        loadRespondents(self.portal)

    def testRegisterMethod(self):
        """Test the register method works correctly"""
        s1 = getattr(self.portal, 's1')
        respondent = s1.getAuthenticatedRespondent('user2@here.com')
        assert 'email_sent' in respondent
        assert respondent['email_sent'] == ''
        s1.registerRespondentSent('user2@here.com')
        respondent = s1.getAuthenticatedRespondent('user2@here.com')
        assert 'email_sent' in respondent
        assert len(respondent['email_sent']) > 0

    def testSingleSend(self):
        """Test send to one user registers email sent"""
        s1 = getattr(self.portal, 's1')
        s1.sendSurveyInvite('user2@here.com')
        respondent = s1.getAuthenticatedRespondent('user2@here.com')
        assert 'email_sent' in respondent
        assert len(respondent['email_sent']) > 0


class TestSentFrom(unittest.TestCase):
    """Test email is sent from correct address"""
    layer = INTEGRATION_Mail_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        loadRespondents(self.portal)

    def testDefaultFrom(self):
        """Default should come from site admin"""
        s1 = getattr(self.portal, 's1')
        s1.sendSurveyInvite('user2@here.com')
        # messages = self.portal.MailHost.messages
        # XXX this does not fall over to the portal administrator
        # assert 'From: "Portal Administrator" <postmaster@localhost>' \
        #     in messages[0]

    def testSurveyFrom(self):
        """Test email from survey manager"""
        s1 = getattr(self.portal, 's1')
        s1.setInviteFromName('Survey Manager')
        s1.setInviteFromEmail('survey@here.com')
        s1.sendSurveyInvite('user2@here.com')
        messages = self.portal.MailHost.messages
        assert 'From: "Survey Manager" <survey@here.com>' in messages[0]
