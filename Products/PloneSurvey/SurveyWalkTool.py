from Products.CMFCore.utils import UniqueObject 
from OFS.SimpleItem import SimpleItem 
from Globals import InitializeClass 
from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping
from persistent.dict import PersistentDict
from Products.PloneSurvey import permissions

class SurveyWalkTool(UniqueObject, SimpleItem): 

    """ The survey walk tool 

 Register the walk of the user in the Survey, and can enable "go back" to previous step

 Uses UID to keep track of Surveys.

 Examples:

 my_survey = context.my_survey
 my_survey_uid = my_survey.UID()

 print st.doStep('yuri', my_survey_uid, 'first subsurvey') -> the user do a step to "first subsurvey"
 st.resetWalks(my_survey_uid) -> reset all walks

""" 

    id = 'surveywalk_tool' 

    meta_type= 'SurveyWalkTool' 

    plone_tool = 1 

    def __init__(self):
        self.resetAll()

    security = ClassSecurityInfo()

    security.declareProtected(permissions.ModifyPortalContent, 'resetAll')
    def resetAll(self):
        """Remove walks for all users """
        self.walks = PersistentDict()

    security.declareProtected(permissions.ModifyPortalContent, 'resetWalks')
    def resetWalks(self, survey):
        """Reset walks for all users, for an existing """
        survey_walk = self.getWalks(survey)
	survey_walk = OOBTree()

    security.declareProtected(permissions.View, 'getWalks')
    def getWalks(self, survey):
        """Get walks for the survey """
	if survey in self.walks.keys():
         return self.walks[survey]
	else:
	 return None

    def registerSurvey(self, survey):
	""" Register a survey, so we can store walks """
	if survey not in self.walks.keys():
	 self.walks[survey] = OOBTree()

    def isRegisteredSurvey(self, survey):
        """ Register a survey, so we can store walks """
        return survey in self.walks.keys()

    security.declareProtected(permissions.ModifyPortalContent, 'resetWalkForUser')
    def resetWalkForUser(self, survey, userid):
        """Remove walk for a single user"""
	survey_walks = self.getWalks(survey)
        if survey_walks.has_key(userid):
            del survey_walks[userid]

    security.declareProtected(permissions.View, 'addWalk')
    def addWalk(self, survey, userid, value, comments=""):
        """Add an walk and optional comments for a user.
        This method protects _addWalk from anonymous users specifying a
        userid when they walk, and thus apparently walking as another user
        of their choice.
        """

	survey_walks = self.getWalks(survey)
        survey_walks[userid] = PersistentMapping(value=value,
                                                 comments=comments)
        if not isinstance(self.walks, (PersistentMapping, OOBTree)):
            # It must be a standard dictionary from an old install, so
            # we need to inform the ZODB about the change manually.
            survey_walks._p_changed = 1

    security.declareProtected(permissions.View, 'getWalkFor')
    def getWalkFor(self, survey, userid):
        """Get a specific user's walk"""
	survey_walks = self.getWalks(survey)
        if survey_walks <> None:
         walk = survey_walks.get(userid, {}).get('value', None)
         return walk
	else:
	 return None

    security.declareProtected(permissions.View, 'getAllWalk')
    def getAllWalk(self, survey):
        """ Get all user's walk """
        walk = []
        for user in self.getAllUsers():
         walk.append((user, self.getWalkFor(user)))
        return walk

    security.declareProtected(permissions.View, 'getAllWalk')
    def getAllUsers(self, survey):
	""" get all users """
	survey_walks = self.getWalks(survey)
	if survey_walks <> None:
	 return survey_walks.keys()
	else:
	 return None

    security.declareProtected(permissions.View, 'doStep')
    def doStep(self, survey, userid, step):
	""" add a path to a walk """
	actual_walk = self.getWalkFor(survey, userid=userid)
	if actual_walk == None:
	 self.addWalk(survey, userid=userid, value = [step])
	else:
	 actual_walk.append(step)
	 self.addWalk(survey = survey, userid = userid , value = actual_walk)
	return (userid, self.getWalkFor(survey, userid=userid))

    security.declareProtected(permissions.View, 'prettyPrintUserWalk')
    def prettyPrintUserWalk(self, survey, userid):
	""" return a pretty printed version of a user walk"""

	walk = self.getWalkFor(survey, userid)
	if walk <> None:
	 return '-> '.join(walk)
	else:
	 return None

InitializeClass(SurveyWalkTool)
