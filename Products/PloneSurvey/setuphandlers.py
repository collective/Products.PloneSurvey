import logging

from zope.component import getUtility

from plone.api import portal
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry

try:
    from Products.CMFPlone.interfaces import INavigationSchema
    HAS_NAV_SCHEMA = True  # plone5
except ImportError:
    HAS_NAV_SCHEMA = False  # plone4


LOGGER_ID = 'Products.PloneSurvey'
PROFILE_ID = 'profile-Products.PloneSurvey:default'


def importVarious(context):
    """
    Import various settings."""
    # Only run step if a flag file is present
    if context.readDataFile('PloneSurvey.txt') is None:
        return

    if HAS_NAV_SCHEMA:
        registry = getUtility(IRegistry)
        navigation_settings = registry.forInterface(INavigationSchema, prefix='plone')
        if 'Survey' not in navigation_settings.displayed_types:
            tmp = tuple(navigation_settings.displayed_types)
            # XXX this doesn't work in registry.xml in tests
            portal.set_registry_record('plone.displayed_types', tmp + ('Survey',))


def nullStep(context, logger=None):
    """Null step"""
    pass


def upgrade_to_1_4_3(context, logger=None):
    """Method to upgrade the profile to version 2.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger(LOGGER_ID)

    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
