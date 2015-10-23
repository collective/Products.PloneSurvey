import unittest

from AccessControl import getSecurityManager

from plone.app.testing import login, logout
from Products.CMFCore.utils import getToolByName
from Testing.testbrowser import Browser

from Products.PloneSurvey import permissions

from base import INTEGRATION_ANON_SURVEY_TESTING, FUNCTIONAL_TESTING


class TestPermissions(unittest.TestCase):
    """Test permissions work correctly"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_membership = getToolByName(self.portal,
                                               'portal_membership')
        # need to log in as another user as the test user has owner role here
        self.portal_membership.addMember(
            'survey_user',
            'secret',
            ['Contributor', ],
            [],
            {'fullname': 'Survey User', 'email': 'survey@here.com', }
        )
        logout()
        login(self.portal, 'survey_user')

    def testResultsPermission(self):
        s1 = getattr(self.portal, 's1')
        assert getSecurityManager().checkPermission(
            permissions.ViewSurveyResults,
            s1
        )


class TestPermissionsFunctional(unittest.TestCase):
    """Test permissions work correctly"""
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser()

    def testResultViewManager(self):
        pass
        # s1 = getattr(self.portal, 's1')
        # self.checkIsUnauthorized(s1.absolute_url() + '/survey_view_results')

    # def testResultsView(self):
        # self.setRoles(['Manager',])
        # self.browser.open(self.folder.absolute_url() +
        #                   '/s1/survey_view_results')
        # assert self.browser.contents.find('Forgot your password?') == -1, \
        #     self.browser.contents

    # def testForbidForMember(self):
        # self.setRoles(['Member',])
        # self.browser.open(self.folder.absolute_url() +
        #                   '/s1/survey_view_results')
        # assert self.browser.contents.find('Forgot your password?') >= 0, \
        #     self.browser.contents
