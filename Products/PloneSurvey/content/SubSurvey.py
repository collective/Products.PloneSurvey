import string
from AccessControl import ClassSecurityInfo
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping
from zope.interface import classImplements

from Products.Archetypes.atapi import *
from Products.Archetypes.interfaces import IMultiPageSchema
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import PROJECTNAME

from schemata import SubSurveySchema

class SubSurvey(ATCTOrderedFolder):
    """A sub page within a survey"""
    schema = SubSurveySchema
    _at_rename_after_creation = True
    portal_type = 'Sub Survey'
    security = ClassSecurityInfo()

    def __init__(self, oid, **kwargs):
        self.reset()
        ATCTOrderedFolder.__init__(self, oid, **kwargs)

    security.declareProtected(permissions.ModifyPortalContent, 'reset')
    def reset(self):
        """Remove answers for all users."""
        self.answers = OOBTree()

    security.declareProtected(permissions.ModifyPortalContent, 'resetForUser')
    def resetForUser(self, userid):
        """Remove answer for a single user"""
        if self.answers.has_key(userid):
            del self.answers[userid]

    def manage_afterClone(self, item):
	# elimino il flag sulla validazione
	self.reset()
        ATCTOrderedFolder.manage_afterClone(self, item)

    security.declareProtected(permissions.View, 'addAnswer')
    def addAnswer(self, value, comments=""):
        """Add an answer and optional comments for a user.
        This method protects _addAnswer from anonymous users specifying a
        userid when they vote, and thus apparently voting as another user
        of their choice.
        """
        # Get hold of the parent survey
        survey = None
        ob = self
        while survey is None:
            ob = ob.aq_inner.aq_parent
            if ob.meta_type == 'Survey':
                survey = ob
            elif getattr(ob, '_isPortalRoot', False):
                raise Exception("Could not find a parent Survey.")
        portal_membership = getToolByName(self, 'portal_membership')
        if portal_membership.isAnonymousUser() and not survey.getAllowAnonymous():
            raise Unauthorized, ("This survey is not available to anonymous users.")
        # Use the survey to get hold of the appropriate userid
        userid = survey.getSurveyId()
        # Call the real method for storing the answer for this user.
        return self._addAnswer(userid, value, comments)

    def _addAnswer(self, userid, value, comments=""):
        """Add an answer and optional comments for a user."""
        # We don't let users over-write answers that they've already made.
        # Their first answer must be explicitly 'reset' before another
        # answer can be supplied.
        # XXX this causes problem when survey fails validation
        # will also cause problem with save function
##        if self.answers.has_key(userid):
##            # XXX Should this get raised?  If so, a more appropriate
##            # exception is probably in order.
##            msg = "User '%s' has already answered this question. Reset the original response to supply a new answer."
##            raise Exception(msg % userid)
##        else:
        self.answers[userid] = PersistentMapping(value=value,
                                                 comments=comments)
        if not isinstance(self.answers, (PersistentMapping, OOBTree)):
            # It must be a standard dictionary from an old install, so
            # we need to inform the ZODB about the change manually.
            self.answers._p_changed = 1

    security.declareProtected(permissions.View, 'getAnswerFor')
    def getAnswerFor(self, userid):
        """Get a specific user's answer"""
        answer = self.answers.get(userid, {}).get('value', None)
        return answer

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        """Doesn't make sense for surveys to allow alternate views"""
        return False

    security.declarePublic('canConstrainTypes')
    def canConstrainTypes(self):
        """Should not be able to add non survey types"""
        return False

    security.declareProtected(permissions.View, 'isMultipage')
    def isMultipage(self):
        """Return true if there is more than one page in the survey"""
        return True

    security.declareProtected(permissions.View, 'getSurveyId')
    def getSurveyId(self):
        """Return the userid for the survey"""
        request = self.REQUEST
        try:
            user_id = request.form['survey_user_id']
        except KeyError:
            pass
        else:
            portal_membership = getToolByName(self, 'portal_membership')
            if not portal_membership.isAnonymousUser():
                if portal_membership.getAuthenticatedMember().getId() == user_id:
                    return user_id
            else:
                survey_cookie = self.aq_parent.getId()
                if self.aq_parent.getAllowAnonymous() and self.REQUEST.has_key(survey_cookie) and request.get(survey_cookie, "Anonymous") == user_id:
                    return user_id
            # XXX survey is probably being spoofed, need another field for allow users without cookies, for now let them through
            return user_id
        survey_url = self.aq_parent.absolute_url()
        return self.REQUEST.RESPONSE.redirect(survey_url)

    security.declareProtected(permissions.ModifyPortalContent, 'getValidationQuestions')
    def getValidationQuestions(self):
        """Return the questions for the validation field"""
        portal_catalog = getToolByName(self, 'portal_catalog')
        questions = [('', 'None')]
        path = string.join(self.aq_inner.aq_parent.getPhysicalPath(), '/')
        results = portal_catalog.searchResults(portal_type = ['Survey Select Question',],
                                               path = path)
        for result in results:
            object = result.getObject()
            questions.append((object.getId(), object.Title() + ', ' + str(object.getQuestionOptions())))
        vocab_list = DisplayList((questions))
        return questions

    security.declareProtected(permissions.View, 'getBranchingCondition')
    def getBranchingCondition(self):
        """Return the title of the branching question"""
        branchings = ''
        required_question = self.getRequiredQuestion()
        branch_question = self[required_question]
        branchings = branch_question.Title()+':'+self.getRequiredAnswer()
        return branchings

    security.declareProtected(permissions.View, 'getQuestions')
    def getQuestions(self):
        """Return the questions for this part of the survey"""
        questions = self.getFolderContents(
            contentFilter={'portal_type':[
                'Survey Matrix',
                'Survey Grid Question',
                'Survey Select Question',
                'Survey Text Question',
                'Survey Two Dimensional',
                ]}, full_objects=True)
        return questions

    security.declareProtected(permissions.View, 'checkCompleted')
    def checkCompleted(self):
        """Return true if this page is completed"""
        # XXX
        return True

    security.declareProtected(permissions.View, 'getNextPage')
    def getNextPage(self):
        """Return the next page of the survey"""
        previous_page = True
	def log_step(survey_tool, userid, step):
            survey_tool.doStep(survey = self.getSurveyRoot().UID(), userid=userid, step=step)
        survey_tool = getToolByName(self, 'plone_survey_tool')
        parent = self.aq_inner.aq_parent
	userid = self.getSurveyId()
        pages = parent.getFolderContents(contentFilter={'portal_type':'Sub Survey',}, full_objects=True)
        for page in pages:
            if previous_page:
                if page.getId() == self.getId():
                     previous_page = False
            elif page.displaySubSurvey():
                log_step(survey_tool, userid, self.id)
                return page()
        return self.exitSurvey()

    security.declareProtected(permissions.View, 'getPreviousPage')
    def getPreviousPage(self):
        """Return the previous page of the survey"""
	survey_tool = getToolByName(self, 'plone_survey_tool')
        #parent = self.aq_inner.aq_parent
	parent = self.getSurveyRoot()
        userid = self.getSurveyId()
	walk = survey_tool.getWalkFor(survey = parent.UID(), userid = userid)
	if walk <> None and walk <> []:	
	   previous = walk[-1]
	   new_walk = list(walk[:-1])
	   survey_tool.addWalk(survey = parent.UID(), userid = userid, value = new_walk)
	else:
	   previous = None
	   return parent()
	return parent[previous]()

    security.declareProtected(permissions.View, 'displaySubSurvey')
    def displaySubSurvey(self):
        """Determine whether this page should be displayed"""
        parent = self.aq_parent
        userid = parent.getSurveyId()
        if hasattr(self, 'getNextsub') and  self.getNextsub() is not None:
            log_step(st, userid, self.id)
            return parent[self.getNextsub()]()
        required_question = self.getRequiredQuestion()
        if not required_question:
             return True
        # find the right question
        # TODO: this assumes that no questions exist with a duplicate id
        if required_question in parent.objectIds():
            question = parent[required_question]
        else:
            pages = parent.getFolderContents(contentFilter={'portal_type':'Sub Survey',}, full_objects=True)
            for page in pages:
                if required_question in page.objectIds():
                    question = page[required_question]
                    break
        # TODO: this assumes the question actually exists
        required_answer = self.getRequiredAnswer().split('|')
        required_positive = self.getRequiredAnswerYesNo()
        answer = question.getAnswerFor(userid)
        if hasattr(answer, 'lower'):
            if required_positive and answer == required_answer:
                return True
            elif answer != required_answer and not required_positive:
                return True
            return False
        elif hasattr(answer, 'append'): # it's a list
            if required_positive and required_answer in answer :
                return True
            elif required_answer not in answer and not required_positive:
                return True
            return False
        else: # question not answered, so don't display
            return False

classImplements(SubSurvey, IMultiPageSchema)
registerATCT(SubSurvey, PROJECTNAME)
