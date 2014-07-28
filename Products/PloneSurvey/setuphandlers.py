import logging

from Products.CMFCore.utils import getToolByName

LOGGER_ID = 'Products.PloneSurvey'
PROFILE_ID = 'profile-Products.PloneSurvey:default'


def importVarious(context):
    """
    Import various settings."""
    # Only run step if a flag file is present
    if context.readDataFile('PloneSurvey.txt') is None:
        return


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
