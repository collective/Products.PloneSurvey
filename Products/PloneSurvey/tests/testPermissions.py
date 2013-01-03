import unittest2 as unittest

from AccessControl import getSecurityManager
from DateTime import DateTime
from ZPublisher.BaseRequest import BaseRequest as Request

from Testing.testbrowser import Browser

from Products.PloneSurvey import permissions

from base import INTEGRATION_TESTING, FUNCTIONAL_TESTING

class TestPermissions(unittest.TestCase):
    """Test permissions work correctly"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.createAnonSurvey()
        # need to log in as another user as the test user has owner role here
        self.addMember('survey_user', 'Survey User', 'survey@here.com', ['Contributor',], DateTime())
        self.logout()
        self.login('survey_user')

    def testResultsPermission(self):
        s1 = getattr(self.folder, 's1')
        assert getSecurityManager().checkPermission(permissions.ViewSurveyResults, s1)

class TestPermissions(unittest.TestCase):
    """Test permissions work correctly"""
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser()

    def testResultViewManager(self):
        s1 = getattr(self.portal, 's1')
        #self.checkIsUnauthorized(s1.absolute_url() + '/survey_view_results')

    #def testResultsView(self):
        #self.setRoles(['Manager',])
        #self.browser.open(self.folder.absolute_url() + '/s1/survey_view_results')
        #assert self.browser.contents.find('Forgot your password?') == -1, self.browser.contents

    #def testForbidForMember(self):
        #self.setRoles(['Member',])
        #self.browser.open(self.folder.absolute_url() + '/s1/survey_view_results')
        ##assert self.browser.contents.find('Forgot your password?') >= 0, self.browser.contents
