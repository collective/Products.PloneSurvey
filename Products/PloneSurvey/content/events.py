
def createSurveyEventHandler(ob, event):
    """Initialise the survey"""
    if not 'acl_users' in ob.objectIds():
        ob.createLocalPas()
    try:
        ob.aq_inner.aq_base.respondents
    except AttributeError:
        ob.reset()

def createQuestionEventHandler(ob, event):
    """Initialise the question"""
    try:
        ob.aq_inner.aq_base.answers
    except AttributeError:
        ob.reset()
