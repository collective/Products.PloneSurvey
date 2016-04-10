# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl.class_init import InitializeClass
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName


class BaseQuestion(ATCTContent):
    """Base class for survey questions"""
    immediate_view = "base_edit"
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ()
    include_default_actions = 1
    _at_rename_after_creation = True
    security = ClassSecurityInfo()

    @security.protected(ModifyPortalContent)
    def reset(self):
        """Remove answers for all users."""
        self.answers = OOBTree()

    @security.protected(ModifyPortalContent)
    def resetForUser(self, userid):
        """Remove answer for a single user"""
        if userid in self.answers:
            del self.answers[userid]

    @security.protected(View)
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
            ob = aq_parent(aq_inner(ob))
            if ob.meta_type == 'Survey':
                survey = ob
            elif getattr(ob, '_isPortalRoot', False):
                raise Exception("Could not find a parent Survey.")
        portal_membership = getToolByName(self, 'portal_membership')
        is_anon = portal_membership.isAnonymousUser()
        if is_anon and not survey.getAllowAnonymous():
            raise Unauthorized(
                "This survey is not available to anonymous users."
            )
        userid = self.getSurveyId()
        if is_anon and userid not in survey.getRespondentsList():
            # anon is not added on survey view, so may need to be added
            survey.addRespondent(userid)
        # Call the real method for storing the answer for this user.
        return self._addAnswer(userid, value, comments)

    def _addAnswer(self, userid, value, comments=""):
        """Add an answer and optional comments for a user."""
        # We don't let users over-write answers that they've already made.
        # Their first answer must be explicitly 'reset' before another
        # answer can be supplied.
        # XXX this causes problem when survey fails validation
        # will also cause problem with save function
#        if self.answers.has_key(userid):
#            # XXX Should this get raised?  If so, a more appropriate
#            # exception is probably in order.
#            msg = "User '%s' has already answered this question.
#                   Reset the original response to supply a new answer."
#            raise Exception(msg % userid)
#        else:
        self.answers[userid] = PersistentMapping(value=value,
                                                 comments=comments)
        if not isinstance(self.answers, (PersistentMapping, OOBTree)):
            # It must be a standard dictionary from an old install, so
            # we need to inform the ZODB about the change manually.
            self.answers._p_changed = 1

    @security.protected(View)
    def getAnswerFor(self, userid):
        """Get a specific user's answer"""
        answer = self.answers.get(userid, {}).get('value', None)
        if self.getInputType() in ['multipleSelect', 'checkbox']:
            if type(answer) == 'NoneType':
                return []
        if self.getInputType() in ['radio', 'selectionBox']:
            if not answer:
                return ""
            if isinstance(answer, unicode):
                answer = answer.encode('utf8')
            return str(answer)
        return answer

    @security.protected(View)
    def getCommentsFor(self, userid):
        """Get a specific user's comments"""
        return self.answers.get(userid, {}).get('comments', None)

    @security.protected(View)
    def getComments(self):
        """Return a userid, comments mapping"""
        mlist = []
        for k, v in self.answers.items():
            mapping = {}
            mapping['userid'] = k
            mapping['comments'] = v.get('comments', '')
            mlist.append(mapping)
        return mlist

    @security.protected(View)
    def getNumberOfRespondents(self):
        return len(self.answers.keys())

    @security.private
    def _get_yes_no_default(self):
        translation_service = getToolByName(self, 'translation_service')
        return (translation_service.utranslate(domain='plonesurvey',
                                               msgid=u'Yes',
                                               context=self),
                translation_service.utranslate(domain='plonesurvey',
                                               msgid=u'No',
                                               context=self), )

    @security.private
    def _get_commentLabel_default(self):
        translation_service = getToolByName(self, 'translation_service')
        return translation_service.utranslate(
            domain='plonesurvey',
            msgid=u'commentLabelDefault',
            default=u'Comment - mandatory if "no"', context=self)

InitializeClass(BaseQuestion)
