#
# Test PloneSurvey permissions
#
from AccessControl import getSecurityManager
from DateTime import DateTime
from ZPublisher.BaseRequest import BaseRequest as Request

from Products.Five.testbrowser import Browser

from Products.PloneSurvey import permissions

from base import PloneSurveyTestCase, BaseFunctionalTestCase

class TestPermissions(PloneSurveyTestCase):
    """Test permissions work correctly"""

    def afterSetUp(self):
        self.createAnonSurvey()
        # need to log in as another user as the test user has owner role here
        self.addMember('survey_user', 'Survey User', 'survey@here.com', ['Contributor',], DateTime())
        self.logout()
        self.login('survey_user')

    def testResultsPermission(self):
        s1 = getattr(self.folder, 's1')
        assert getSecurityManager().checkPermission(permissions.ViewSurveyResults, s1)

class TestPermissions(BaseFunctionalTestCase):
    """Test permissions work correctly"""

    def afterSetUp(self):
        self.browser = Browser()
        self.createAnonSurvey()

    def testResultViewManager(self):
        s1 = getattr(self.folder, 's1')
        #self.checkIsUnauthorized(s1.absolute_url() + '/survey_view_results')

    #def testResultsView(self):
        #self.setRoles(['Manager',])
        #self.browser.open(self.folder.absolute_url() + '/s1/survey_view_results')
        #assert self.browser.contents.find('Forgot your password?') == -1, self.browser.contents

    #def testForbidForMember(self):
        #self.setRoles(['Member',])
        #self.browser.open(self.folder.absolute_url() + '/s1/survey_view_results')
        ##assert self.browser.contents.find('Forgot your password?') >= 0, self.browser.contents
