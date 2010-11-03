import logging

from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

def importVarious(context):
    """
    Import various settings."""
    # Only run step if a flag file is present
    if context.readDataFile('PloneSurvey.txt') is None:
        return
    site = context.getSite()
    out = StringIO()

def registerWithSurveyTool(portal, logger=None):
    """Register all of the existing surveys with the survey tool"""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('Products.PloneSurvey')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile('Products.PloneSurvey:default', 'toolset')
    survey_tool = getToolByName(portal, 'plone_survey_tool')
    catalog = getToolByName(portal, 'portal_catalog')
    results = catalog.searchResults(portal_type='Survey')
    for result in results:
        survey = result.getObjecy()
        survey_uid = survey.UID()
        survey_tool.registerSurvey(survey_uid)
    logger.info("%s surveys added to the survey tool." % len(results))
