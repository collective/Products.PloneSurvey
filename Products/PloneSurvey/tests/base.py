"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.

Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""
import os

from Testing import ZopeTestCase
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

# Let Zope know about the two products we require above-and-beyond a basic
# Plone install (PloneTestCase takes care of these).
ZopeTestCase.installProduct('PloneSurvey')

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

from Products.PloneSurvey.config import DEFAULT_SURVEY_INVITE
from Products.PloneSurvey.tests import utils
from Products.CMFPlone.tests.utils import MockMailHost

# Set up a Plone site, and apply the extension profiles
# to make sure they are installed.
setupPloneSite(extension_profiles=('Products.PloneSurvey:default',))

class PloneSurveyTestCase(PloneTestCase):
    """Base class for integration tests for the 'PloneSurvey' product.
    """

    def addMember(self, username, fullname, email, roles, last_login_time):
        self.portal.portal_membership.addMember(username, 'secret', roles, [])
        member = self.portal.portal_membership.getMemberById(username)
        member.setMemberProperties({'fullname': fullname, 'email': email,
                                    'last_login_time': DateTime(last_login_time),})

    def useMockMailHost(self):
        self.portal.MailHost = MockMailHost('MailHost')

    def createAnonSurvey(self):
        """Create an open survey"""
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(('Reviewer',))
        self.workflow.doActionFor(self.s1,'publish')
        self.setRoles(('Member',))
        self.s1.setEmailInvite(DEFAULT_SURVEY_INVITE)

    def createSubSurvey(self):
        """Create a survey with a sub survey"""
        self.createAnonSurvey()
        self.s1.invokeFactory('Sub Survey', 'ss1')
        self.setRoles(('Reviewer',))
        self.workflow.doActionFor(self.s1.ss1,'publish')
        self.setRoles(('Member',))

    def createSimpleTwoPageSurvey(self):
        """Create a survey with some questions"""
        self.createSubSurvey()
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        self.s1.ss1.invokeFactory('Survey Text Question', 'stq2')
        self.setRoles(('Reviewer',))
        self.workflow.doActionFor(self.s1.ss1.stq1,'publish')
        self.workflow.doActionFor(self.s1.ss1.stq2,'publish')
        self.setRoles(('Member',))

    def createBranchingSurvey(self):
        """Create a survey with branching"""
        self.createAnonSurvey()
        self.s1 = getattr(self.folder, 's1')
        self.s1.invokeFactory('Sub Survey', 'ss1')
        self.s1.invokeFactory('Sub Survey', 'ss2')
        self.s1.invokeFactory('Sub Survey', 'ss3')
        self.ss1 = getattr(self.s1, 'ss1')
        self.ss2 = getattr(self.s1, 'ss2')
        self.ss3 = getattr(self.s1, 'ss3')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        self.ss1.invokeFactory('Survey Select Question', 'ssq2')
        self.ss2.invokeFactory('Survey Select Question', 'ssq3')
        self.ss1.setRequiredQuestion('ssq1')
        self.ss1.setRequiredAnswer('No')
        self.ss2.setRequiredQuestion('ssq1')
        self.ss2.setRequiredAnswer('Yes')
        self.ss3.setRequiredQuestion('ssq2')
        self.ss3.setRequiredAnswer('Yes')

    def loadRespondents(self):
        """Load the test respondents"""
        data_path = os.path.dirname(utils.__file__)
        data_catch = open(os.path.join(data_path, 'user_import'), 'rU')
        input = data_catch.read()
        data_catch.close()
        self.s1.uploadRespondents(input=input)

    def fixLineEndings(self, txt):
        if txt.count('\r\n'): # MS DOS
            txt = txt.replace('\r\n', '\n')
        elif txt.count('\r'): # Mac
            txt = txt.replace('\r', '\n')
        return txt

class BaseFunctionalTestCase(FunctionalTestCase):
    """ This is a base class for functional test cases for PloneSurvey.
    """

    def checkIsUnauthorized(self, url):
        """
        Check whether URL gives Unauthorized response.
        """
    
        import urllib2
    
        # Disable redirect on security error
        self.portal.acl_users.credentials_cookie_auth.login_path = ""
    
        # Unfuse exception tracking for debugging
        # as set up in afterSetUp()
        self.browser.handleErrors = True
    
        def raising(self, info):
            pass
        self.portal.error_log._ignored_exceptions = ("Unauthorized")
        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising
    
        try:
            self.browser.open(url)
            raise AssertionError("No Unauthorized risen:" + url)
        except urllib2.HTTPError,  e:
            # Mechanize, the engine under testbrowser
            # uses urlllib2 and will raise this exception
            self.assertEqual(e.code, 401, "Got HTTP response code:" + str(e.code))

    def createAnonSurvey(self):
        """Create an open survey"""
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(('Reviewer',))
        self.workflow.doActionFor(self.s1,'publish')
        self.setRoles(('Member',))
        self.s1.setEmailInvite(DEFAULT_SURVEY_INVITE)
