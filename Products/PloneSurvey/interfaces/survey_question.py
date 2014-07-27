from zope.interface import Interface


class IPloneSurveyQuestion(Interface):
    """A question within a survey"""

    def reset():
        """Remove answers for all users."""

    def resetForUser(userid):
        """Remove answer for a single user"""

    def addAnswer(value, comments=""):
        """Add an answer and optional comments for a user.
        This method protects _addAnswer from anonymous users specifying a
        userid when they vote, and thus apparently voting as another user
        of their choice.
        """

    def _addAnswer(userid, value, comments=""):
        """Add an answer and optional comments for a user."""

    def getAnswerFor(userid):
        """Get a specific user's answer"""

    def getCommentsFor(userid):
        """Get a specific user's comments"""

    def getComments():
        """Return a userid, comments mapping"""
