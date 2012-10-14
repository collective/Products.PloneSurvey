import os
import datetime

from zope.component import getSiteManager

from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, setRoles

from plone.testing import z2

from Products.ATContentTypes.utils import dt2DT
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

from Products.PloneSurvey.config import PROJECTNAME

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
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='fixture:Integration')
