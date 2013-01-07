questions = context.getAllQuestionsInOrder()
_ = context.translate 

if not questions:
    context.plone_utils.addPortalMessage(_(u'There are no questions to reset.'), 'error')
    return state.set(status='failure')

for question in questions:
    question.reset()

question.aq_parent.setCompletedFor([])

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Survey did not reset correctly.'), 'error')
    return state.set(status='failure')
else:
    context.plone_utils.addPortalMessage(_(u'Survey has been reset.'), 'info')
    return state.set(status='success')
