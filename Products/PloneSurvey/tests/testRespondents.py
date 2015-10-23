import unittest

import os

from Products.PloneSurvey.tests import utils

from base import INTEGRATION_ANON_SURVEY_TESTING


class TestUploadMembers(unittest.TestCase):
    """Test Upload members"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def testUploadMethod(self):
        s1 = getattr(self.portal, 's1')
        assert len(s1.getAuthenticatedRespondents()) == 0
        data_path = os.path.dirname(utils.__file__)
        data_catch = open(os.path.join(data_path, 'user_import'), 'rU')
        input = data_catch.read()
        data_catch.close()
        s1.uploadRespondents(input=input)
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 2
        respondent = s1.getAuthenticatedRespondent('user2@here.com')
        assert respondent['fullname'] == 'User Two'


class TestDeleteMember(unittest.TestCase):
    """Test member deletion"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        data_path = os.path.dirname(utils.__file__)
        data_catch = open(os.path.join(data_path, 'user_import'), 'rU')
        input = data_catch.read()
        data_catch.close()
        self.portal.s1.uploadRespondents(input=input)

    def testDeleteRespondent(self):
        """Ensure a respondent can be deleted"""
        s1 = getattr(self.portal, 's1')
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 2
        s1.deleteAuthenticatedRespondent('user1@here.com')
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 1
        assert respondents[0]['fullname'] == 'User Two'

    def testDeleteProperties(self):
        """Ensure respondents details deleted"""
        s1 = getattr(self.portal, 's1')
        s1.deleteAuthenticatedRespondent('user2@here.com')
        assert s1.getAuthenticatedRespondents()[0]['email_sent'] == ''
        s1.registerRespondentSent('user1@here.com')
        assert s1.getAuthenticatedRespondents()[0]['email_sent'] != ''
        s1.deleteAuthenticatedRespondent('user1@here.com')
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 0
        data_path = os.path.dirname(utils.__file__)
        data_catch = open(os.path.join(data_path, 'user_import'), 'rU')
        input = data_catch.read()
        data_catch.close()
        s1.uploadRespondents(input=input)
        s1.deleteAuthenticatedRespondent('user2@here.com')
        assert s1.getAuthenticatedRespondents()[0]['email_sent'] == '', \
            'Known error'
