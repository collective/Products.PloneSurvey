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

swt = context.surveywalk_tool
survey_id = context.getSurveyRoot().UID()

users = swt.getAllUsers(survey_id)

if users <> None:
 for user in users:
  print user, ':', swt.prettyPrintUserWalk(context.getSurveyRoot().UID(), user)

return printed
