form = context.REQUEST.form
_ = context.translate
questions = context.getQuestions()

if form.get('form.button.save', ''):
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
                value = form.get(q.getId() + '-' + matrix_q.getId(), '')
                matrix_q.addAnswer(value)
    return state.set(status='success')

for q in questions:
    value = form.get(q.getId(), '')
    if q.portal_type == 'Survey Matrix':
        pass
    elif q.getRequired() and not value and (q.portal_type not in ['Survey Two Dimensional', 'Survey Date Question']):
        error_msg = _(msgid='please_provide_answer',
            default=u'Please provide an answer for this question',
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
    elif q.portal_type == 'Survey Select Question':
        q.validateAnswer(value, comments, state)
    elif q.portal_type not in ('Survey Matrix', 'Survey Two Dimensional'):
        q.addAnswer(value, comments)
    elif q.portal_type in ('Survey Matrix',):
        q.validateAnswer(form, state)
    elif q.portal_type in ('Survey Matrix', 'Survey Two Dimensional'):
        matrix_questions = q.getQuestions()
        qnum = ''
        for matrix_q in matrix_questions:
            matrix_qid = str(q.getId()) + '-' + str(matrix_q.getId())
            value = form.get(matrix_qid, '')
            try:
                value = int(value)
            except TypeError:
                # most probably we have multiple selects
                newvalue = []
                for number in value:
                    try:
                        newvalue.append(int(number))
                    except ValueError:
                        newvalue.append(number)
                value = newvalue
            except ValueError:
                pass
            if matrix_q.getRequired() and not value and not value == 0:
               qnum = qnum + ' ' + str(matrix_q.title_or_id()) + ','
            matrix_q.addAnswer(value)
        if qnum != '':
            qnum = qnum[:-1]
            error_msg = _(msgid='please_provide_answer',
                default=u'Please provide an answer for this question',
                domain='plonesurvey')
            state.setError(q.getId(), "%s %s" % (error_msg, qnum))

if not state.getErrors():
    if context.getShowCaptcha() and not context.hasMorePages():
        if context.isCaptchaInstalled():
            context.captcha_validator()
        else:
            recaptcha_verify = context.restrictedTraverse('@@captcha/verify', None)
            if recaptcha_verify:
                try:
                    if not recaptcha_verify():
                        error_msg = _(msgid='captcha_code_wrong',
                            default=u'Captcha protection code is wrong. Please retry.',
                            domain='plonesurvey')
                        state.setError('recaptcha_response_field', error_msg)
                except ValueError:
                    # No recaptcha private key configured
                    pass

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the errors shown.'), 'error')
    return state.set(status='failure')
else:
    state.set(status='success')
    state.setKwargs({'survey_user_id':form.get('survey_user_id')})
    return state
return state
