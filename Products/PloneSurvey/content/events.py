
def createSurveyEventHandler(ob, event):
    """Initialise the survey"""
    if not 'acl_users' in ob.objectIds():
        ob.createLocalPas()
    try:
        respondents = ob.respondents
    except AttributeError:
        ob.reset()

def createQuestionEventHandler(ob, event):
    """Initialise the question"""
    try:
        answers = ob.answers
    except AttributeError:
        ob.reset()
