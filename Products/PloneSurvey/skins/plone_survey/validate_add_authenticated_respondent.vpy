_ = context.translate
acl_users = context.get_acl_users()

fullname = context.REQUEST.get('fullname', '').strip()
emailaddress = context.REQUEST.get('emailaddress', '').strip()

if not fullname:
    error_msg = context.translate(
        default='Please provide a name',
        msgid='please_provide_fullname',
        domain='plonesurvey')
    state.setError('fullname', error_msg)

if not emailaddress:
    error_msg = context.translate(
        default='Please provide an email address',
        msgid='please_provide_email_address',
        domain='plonesurvey')
    state.setError('emailaddress', error_msg)

# Validate email address
reg_tool = context.portal_registration
if not reg_tool.isValidEmail(emailaddress):
    error_msg = context.translate(
        default='The email address is invalid',
        msgid='email_address_invalid',
        domain='plonesurvey')
    state.setError('emailaddress', error_msg)

# Check that it is not in use already
if emailaddress in acl_users.getUserNames():
    error_msg = context.translate(
        default='The email address is already in use',
        msgid='email_address_in_use',
        domain='plonesurvey')
    state.setError('emailaddress', error_msg)


if state.getErrors():
    return state.set(status='failure', portal_status_message=_(msgid='text_correct_errors', default=u'Please correct the errors', domain='plonesurvey'))
else:
    context.addAuthenticatedRespondent(emailaddress, fullname=fullname)
    return state.set(status='success',
        portal_status_message=_(msgid='authenticated_respondent_created', default=u'Respondent created', domain='plonesurvey'))
