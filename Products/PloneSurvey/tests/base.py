import os

from zope.component import getSiteManager

from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, setRoles

from plone.testing import z2

from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.config import DEFAULT_SURVEY_INVITE
from Products.PloneSurvey.tests import utils


class TestCase(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneSurvey
        self.loadZCML(package=Products.PloneSurvey)

        # Install product and call its initialize() function
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, '%s:default' % PROJECTNAME)

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, PROJECTNAME)

FIXTURE = TestCase()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,),
                                         name='fixture:Integration')


class TestAnonCase(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneSurvey
        self.loadZCML(package=Products.PloneSurvey)

        # Install product and call its initialize() function
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, '%s:default' % PROJECTNAME)
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Survey', 's1')
        s1 = getattr(portal, 's1')
        s1.setAllowAnonymous(True)
        # workflow_tool = getToolByName(portal, 'portal_workflow')
        # workflow_tool.doActionFor(s1,'publish')
        s1.setEmailInvite(DEFAULT_SURVEY_INVITE)

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, PROJECTNAME)

ANON_FIXTURE = TestAnonCase()
INTEGRATION_ANON_SURVEY_TESTING = IntegrationTesting(bases=(ANON_FIXTURE,),
                                                     name='fixture:Anon')


class TestMailCase(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneSurvey
        self.loadZCML(package=Products.PloneSurvey)

        # Install product and call its initialize() function
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, '%s:default' % PROJECTNAME)
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Survey', 's1')
        s1 = getattr(portal, 's1')
        s1.setAllowAnonymous(True)
        # workflow_tool = getToolByName(portal, 'portal_workflow')
        # workflow_tool.doActionFor(s1,'publish')
        s1.setEmailInvite(DEFAULT_SURVEY_INVITE)
        portal._original_MailHost = portal.MailHost
        portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, PROJECTNAME)

MAIL_FIXTURE = TestMailCase()
INTEGRATION_Mail_TESTING = IntegrationTesting(bases=(MAIL_FIXTURE,),
                                              name='fixture:Mail')


class TestBranchingCase(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneSurvey
        self.loadZCML(package=Products.PloneSurvey)

        # Install product and call its initialize() function
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, '%s:default' % PROJECTNAME)
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Survey', 's1')
        s1 = getattr(portal, 's1')
        s1.setAllowAnonymous(True)
        # workflow_tool = getToolByName(portal, 'portal_workflow')
        # workflow_tool.doActionFor(s1,'publish')
        s1.setEmailInvite(DEFAULT_SURVEY_INVITE)
        s1.invokeFactory('Sub Survey', 'ss1')
        s1.invokeFactory('Sub Survey', 'ss2')
        s1.invokeFactory('Sub Survey', 'ss3')
        ss1 = getattr(s1, 'ss1')
        ss2 = getattr(s1, 'ss2')
        ss3 = getattr(s1, 'ss3')
        s1.invokeFactory('Survey Select Question', 'ssq1')
        ss1.invokeFactory('Survey Select Question', 'ssq2')
        ss2.invokeFactory('Survey Select Question', 'ssq3')
        ss1.setRequiredQuestion('ssq1')
        ss1.setRequiredAnswer('No')
        ss2.setRequiredQuestion('ssq1')
        ss2.setRequiredAnswer('Yes')
        ss3.setRequiredQuestion('ssq2')
        ss3.setRequiredAnswer('Yes')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, PROJECTNAME)

BRANCHING_FIXTURE = TestBranchingCase()
INTEGRATION_BRANCHING_TESTING = IntegrationTesting(bases=(BRANCHING_FIXTURE,),
                                                   name='fixture:Branching')


class FunctionalTestCase(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneSurvey
        self.loadZCML(package=Products.PloneSurvey)

        # Install product and call its initialize() function
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, '%s:default' % PROJECTNAME)
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Survey', 's1')
        s1 = getattr(portal, 's1')
        s1.setAllowAnonymous(True)
        # workflow_tool = getToolByName(portal, 'portal_workflow')
        # workflow_tool.doActionFor(s1,'publish')
        s1.setEmailInvite(DEFAULT_SURVEY_INVITE)

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, PROJECTNAME)

FUNCTIONAL_FIXTURE = FunctionalTestCase()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FUNCTIONAL_FIXTURE,),
                                       name='fixture:Functional')


class ReCaptchaTestCase(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneSurvey
        self.loadZCML(package=Products.PloneSurvey)
        import collective.recaptcha
        self.loadZCML(package=collective.recaptcha)

        # Install product and call its initialize() function
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, '%s:default' % PROJECTNAME)

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, PROJECTNAME)

FIXTURE = ReCaptchaTestCase()
INTEGRATION_RECAPTCHA_TESTING = IntegrationTesting(bases=(FIXTURE,),
                                                   name='fixture:ReCaptcha')


def loadRespondents(portal):
    """Load the test respondents"""
    data_path = os.path.dirname(utils.__file__)
    data_catch = open(os.path.join(data_path, 'user_import'), 'rU')
    input = data_catch.read()
    data_catch.close()
    portal.s1.uploadRespondents(input=input)


def fixLineEndings(txt):
    if txt.count('\r\n'):  # MS DOS
        txt = txt.replace('\r\n', '\n')
    elif txt.count('\r'):  # Mac
        txt = txt.replace('\r', '\n')
    return txt
