userid = context.getSurveyId()
form = context.REQUEST.form
_ = context.translate 

context.resetForUser(userid)

if state.getErrors():
    return state.set(status='failure', portal_status_message=_(msgid='text_correct_errors', domain='plonesurvey', default='Please correct the errors shown'))
else:
    return state.set(status='success')
return state