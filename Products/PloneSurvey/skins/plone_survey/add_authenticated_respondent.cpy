## Controller Python Script "add_authenticated_respondent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=fullname,emailaddress
##title=Add an Authenticated Respondent
##

_ = context.translate

context.addAuthenticatedRespondent(emailaddress, fullname=fullname)

return state.set(status='success', 
    portal_status_message=_(msgid='authenticated_respondent_created', domain='plonesurvey', default='Respondent created'))
