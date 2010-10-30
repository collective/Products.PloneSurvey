form = context.REQUEST.form
_ = context.translate
questions = context.getQuestions()

if form.get('form.button.save', '') or form.get('form.button.getback', ''):
    # skip validation
    for q in questions:
        value = form.get(q.getId(), '')
        comments = form.get("%s_comments" % q.getId(), '')
        if q.portal_type == 'Survey Select Question' and q.getLikertOptions():
            q.addAnswer(int(value), comments)
        elif q.portal_type not in ('Survey Matrix', 'Survey Two Dimensional'):
            q.addAnswer(value, comments)
        else:
            matrix_questions = q.getQuestions()
            for matrix_q in matrix_questions:
                # value = form.get(matrix_q.getId(), '')
	        matrix_qid = str(q.getId()) + '-' + str(matrix_q.getId())
	        value = form.get(matrix_qid, '')
		matrix_q.addAnswer(value)
    return state.set(status='success')

for q in questions:
    value = form.get(q.getId(), '')
    if q.portal_type == 'Survey Matrix' or q.portal_type == 'Survey Grid Question':
	# the validation of required field is done down
        pass
    elif q.getRequired() and not value and (q.portal_type not in ['Survey Two Dimensional', 'Survey Date Question']):
        error_msg = context.translate(
            default=q.pretty_title_or_id() + ': Please provide an answer for this question',
            msgid='please_provide_answer',
            domain='plonesurvey')
        state.setError(q.getId(), error_msg)
    if value and hasattr(q, 'getValidation') and q.getValidation() != 'None':
        validation_output = q.validateQuestion(value)
        if validation_output != 1:
            state.setError(q.getId(), validation_output)
    comments = form.get("%s_comments" % q.getId(), '')
    if q.portal_type == 'Survey Text Question':
        q.validateAnswer(value, state)
    elif q.portal_type == 'Survey Date Question':
        q.validateAnswer(form, q.getId(), state)
    elif q.portal_type == 'Survey Grid Question' and q.getRequired():
        q.validateAnswer(form, state)
    elif q.portal_type == 'Survey Select Question':
        q.validateAnswer(value, comments, state)
    elif q.portal_type not in ('Survey Matrix', 'Survey Two Dimensional'):
        q.addAnswer(value, comments)
    elif q.portal_type in ('Survey Matrix',):
        q.validateAnswer(form, state)

if not state.getErrors():
    if context.getShowCaptcha():
        if context.portal_quickinstaller.isProductInstalled('quintagroup.plonecaptchas'):
            context.captcha_validator()
    
if state.getErrors():
    return state.set(status='failure', portal_status_message=_(msgid='text_correct_errors', domain='plonesurvey', default='Please correct the errors shown'))
else:
    if context.portal_type == 'Survey':
      pass
    else:
      if context.portal_type == 'Sub Survey':
      # qui posso salvare una variabile per indicare che il sub survey e' stato validato
      # context e' il nostro sub survey appena validato
      #  state.setError('va', context.id)
      #  return state.set(status='failure', portal_status_message=_(msgid='text_correct_errors', domain='plonesurvey', default='Please correct the errors shown'))
       context.addAnswer('validato')

    state.set(status='success')
    state.setKwargs({'survey_user_id':form.get('survey_user_id')})
    return state
return state
