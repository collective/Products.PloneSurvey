## Script (Python) "mostra_strade"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

#BBB to rename in show_walks or similar, and convert to a browser view
from Products.CMFCore.utils import getToolByName

survey_tool = getToolByName(self, 'plone_survey_tool')
survey_id = context.getSurveyRoot().UID()

users = survey_tool.getAllUsers(survey_id)

if users <> None:
 for user in users:
  print user, ':', survey_tool.prettyPrintUserWalk(context.getSurveyRoot().UID(), user)

return printed
