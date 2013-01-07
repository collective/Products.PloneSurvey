form = context.REQUEST.form
_ = context.translate

users = form['users']
users_reset = []
if  not users:
    pass
elif not isinstance(users, str):
    for user in users:
        context.resetForUser(user)
        users_reset.append(user)
else:
    context.resetForUser(users)
    users_reset.append(users)

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Survey did not reset correctly.'), 'error')
    return state.set(status='failure')
else:
    context.plone_utils.addPortalMessage(_(u'${users} have been reset.', mapping={'users':users}), 'info')
    return state.set(status='success')
return state
