from zope.interface import Interface, Attribute

class ISurvey(Interface):
    """You can add questions to surveys"""    

    def isMultipage(self):
        """Return true if there is more than one page in the survey"""

    def getQuestions(self):
        """Return the questions for this part of the survey"""

    def getAllQuestions(self):
        """Return all the questions in the survey"""

    def getAllQuestionsInOrder(self, include_sub_survey=False):
        """Return all the questions in the survey"""

    def getNextPage(self):
        """Return the next page of the survey"""

    def exitSurvey(self):
        """Return the defined exit url"""

    def saveSurvey(self):
        """Return the defined exit url"""

    def setCompletedForUser(self):
        """Set completed for a user"""

    def checkCompletedFor(self, user_id):
        """Check whether a user has completed the survey"""

    def getSurveyId(self):
        """Return the userid for the survey"""

    def getAnonymousId(self):
        """ """

    def getRespondents(self):
        """Return a list of respondents"""

    def getAnswersByUser(self, userid):
        """Return a set of answers by user id"""

    def getQuestionsCount(self):
        """Return a count of questions asked"""

    def getSurveyColors(self, num_options):
        """Return the colors for the barchart"""

    def buildSpreadsheetUrl(self):
        """Create a filename for the spreadsheets"""

    def resetForAuthenticatedUser(self):
        """ """

    def resetForUser(self, userid):
        """Remove answer for a single user"""

    def send_email(self, userid):
        """ Send email to nominated address """

    def translateThankYouMessage(self):
        """ """

    def translateSavedMessage(self):
        """ """
