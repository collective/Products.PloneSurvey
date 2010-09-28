
def createSurveyEventHandler(ob, event):
    """Initialise the survey"""
    if not 'acl_users' in ob.objectIds():
        ob.createLocalPas()
