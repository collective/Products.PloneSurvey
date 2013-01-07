userid = context.getSurveyId()
form = context.REQUEST.form
_ = context.translate 

context.resetForAuthenticatedUser()

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the errors shown.'), 'error')
    return state.set(status='failure')
else:
    return state.set(status='success')
return state