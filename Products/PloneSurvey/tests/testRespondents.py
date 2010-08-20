#
# Test PloneSurvey respondents
#
import os

from Products.PloneSurvey.tests import utils
from base import PloneSurveyTestCase

class TestUploadMembers(PloneSurveyTestCase):
    """Test Upload members"""

    def afterSetUp(self):
        self.createAnonSurvey()

    def testUploadMethod(self):
        s1 = getattr(self.folder, 's1')
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


class TestDeleteMember(PloneSurveyTestCase):
    """Test member deletion"""

    def afterSetUp(self):
        self.createAnonSurvey()
        data_path = os.path.dirname(utils.__file__)
        data_catch = open(os.path.join(data_path, 'user_import'), 'rU')
        input = data_catch.read()
        data_catch.close()
        self.s1.uploadRespondents(input=input)

    def testDeleteRespondent(self):
        """Ensure a respondent can be deleted"""
        s1 = getattr(self.folder, 's1')
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 2
        s1.deleteAuthenticatedRespondent('user1@here.com')
        respondents = s1.getAuthenticatedRespondents()
        assert len(respondents) == 1
        assert respondents[0]['fullname'] == 'User Two'

    def testDeleteProperties(self):
        """Ensure respondents details deleted"""
        s1 = getattr(self.folder, 's1')
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
        self.s1.uploadRespondents(input=input)
        s1.deleteAuthenticatedRespondent('user2@here.com')
        assert s1.getAuthenticatedRespondents()[0]['email_sent'] == '', 'Known error'

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUploadMembers))
    suite.addTest(makeSuite(TestDeleteMember))
    return suite
