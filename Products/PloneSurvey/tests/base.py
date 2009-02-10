"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.

Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""

from Testing import ZopeTestCase
from DateTime import DateTime

# Let Zope know about the two products we require above-and-beyond a basic
# Plone install (PloneTestCase takes care of these).
ZopeTestCase.installProduct('PloneSurvey')

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

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

