## Script (Python) "upgrade"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
uid =  context.UID()

# BBB to convert to an upgrade step
from Products.CMFCore.utils import getToolByName

survey_tool = getToolByName(self, 'plone_survey_tool')
survey_tool.registerSurvey(uid)

return 'upgrade done'


