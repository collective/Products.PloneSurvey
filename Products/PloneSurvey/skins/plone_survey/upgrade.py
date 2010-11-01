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
st = context.surveywalk_tool
st.registerSurvey(uid)

return 'upgrade done'


