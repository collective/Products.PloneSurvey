questions = context.getAllQuestionsInOrder()
_ = context.translate 

for question in questions:
    question.reset()

question.aq_parent.setCompletedFor([])

if state.getErrors():
    return state.set(status='failure', portal_status_message=_(msgid='text_survey_reset_error', default=u'Survey did not reset correctly', domain='plonesurvey'))
else:
    return state.set(status='success', portal_status_message=_(msgid='text_survey_reset_success', default=u'Survey has been reset', domain='plonesurvey'))
return state