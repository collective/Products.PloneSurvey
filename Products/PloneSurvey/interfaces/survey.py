from zope.interface import Interface


class ISurvey(Interface):
    """You can add questions to surveys"""

    def isMultipage():
        """Return true if there is more than one page in the survey"""

    def getQuestions():
        """Return the questions for this part of the survey"""

    def getAllQuestions():
        """Return all the questions in the survey"""

    def getAllQuestionsInOrder(include_sub_survey=False):
        """Return all the questions in the survey"""

    def getNextPage():
        """Return the next page of the survey"""

    def exitSurvey():
        """Return the defined exit url"""

    def saveSurvey():
        """Return the defined exit url"""

    def setCompletedForUser():
        """Set completed for a user"""

    def checkCompletedFor(user_id):
        """Check whether a user has completed the survey"""

    def getSurveyId():
        """Return the userid for the survey"""

    def getAnonymousId():
        """ """

    def getAnswersByUser(userid):
        """Return a set of answers by user id"""

    def getQuestionsCount():
        """Return a count of questions asked"""

    def getSurveyColors(num_options):
        """Return the colors for the barchart"""

    def buildSpreadsheetUrl():
        """Create a filename for the spreadsheets"""

    def resetForAuthenticatedUser():
        """ """

    def resetForUser(userid):
        """Remove answer for a single user"""

    def send_email(userid):
        """ Send email to nominated address """

    def translateThankYouMessage():
        """ """

    def translateSavedMessage():
        """ """
