from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import COMMENT_TYPE, TEXT_LOCATION

BaseQuestionSchema = ATContentTypeSchema.copy() + Schema((

    BooleanField('required',
        searchable=0,
        required=0,
        default=1,
        widget=BooleanWidget(
            label="Required",
            label_msgid="label_required",
            description="Select if this question is required, meaning participant must give a response.",
            description_msgid="help_required",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('commentType',
        schemata="Comment Field",
        searchable=0,
        required=0,
        vocabulary=COMMENT_TYPE,
        widget=SelectionWidget(
            label="Comment Type",
            label_msgid="label_comment_type",
            description="Select what type of comment box you would like.",
            description_msgid="help_label_comment_type",
            format="select",
            i18n_domain="plonesurvey",
          )
        ),

    StringField('commentLabel',
        schemata="Comment Field",
        searchable=0,
        required=0,
        default="Comment - mandatory if \"no\"",
        widget=StringWidget(
            label="Comment label",
            label_msgid="label_comment_label",
            description="The comment label.",
            description_msgid="help_comment_label",
            i18n_domain="plonesurvey",
          )
        ),

    TextField('body',
        schemata="Text Block",
        searchable=0,
        required=0,
        default_content_type='text/html',
        default_output_type='text/x-html-safe',
        allowable_content_types=('text/structured',
                                 'text/restructured',
                                 'text/html',
                                 'text/plain',),
        widget=RichWidget(
            label="Text Block",
            label_msgid="XXX",
            i18n_domain="plonesurvey",
           ),
        ),

    IntegerField('textLocation',
        schemata="Text Block",
        searchable=0,
        required=0,
        default=0,
        vocabulary=TEXT_LOCATION,
        widget=SelectionWidget(
            format="radio",
            label="Location of Text Block",
            label_msgid="XXX",
            description="Select where the text block above should appear.",
            description_msgid="XXX",
            i18n_domain="plonesurvey",
           ),
        ),

##    LinesField('dimensions',
##        searchable=0,
##        required=0,
##        default=[],
##        multiValued=1,
##        vocabulary='getDimensionsVocab',
##        widget=MultiSelectionWidget(
##            format='checkbox',
##            label="Dimensions",
##            label_msgid="label_dimensions",
##            description="""Specify the dimensions which apply to this question.""",
##            description_msgid="help_dimensions",
##            i18n_domain="plonesurvey",),
##        index='FieldIndex'
##        ),

    ))

BaseQuestionSchema["title"].widget.label = "Question"
BaseQuestionSchema["description"].widget.label = "Description"
BaseQuestionSchema["description"].widget.label_msgid = "label_question_description"
BaseQuestionSchema["description"].widget.description = "Add a long description of the question here, to clarify any details."
BaseQuestionSchema["description"].widget.description_msgid = "help_question_description"
BaseQuestionSchema["description"].widget.i18n_domain = "plonesurvey"

class BaseQuestion(ATCTContent):
    """Base class for survey questions"""
    immediate_view = "base_edit"
    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ()
    include_default_actions = 1
    _at_rename_after_creation = True

    def __init__(self, oid, **kwargs):
        self.reset()
        BaseContent.__init__(self, oid, **kwargs)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.ModifyPortalContent, 'reset')
    def reset(self):
        """Remove answers for all users."""
        self.answers = OOBTree()

    security.declareProtected(permissions.ModifyPortalContent, 'resetForUser')
    def resetForUser(self, userid):
        """Remove answer for a single user"""
        if self.answers.has_key(userid):
            del self.answers[userid]

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
            ob = ob.aq_parent
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
        if self.getInputType() in ['multipleSelect', 'checkbox']:
            if type(answer) == 'NoneType':
                return []
        return answer

    security.declareProtected(permissions.View, 'getCommentsFor')
    def getCommentsFor(self, userid):
        """Get a specific user's comments"""
        return self.answers.get(userid, {}).get('comments', None)

    security.declareProtected(permissions.View, 'getComments')
    def getComments(self):
        """Return a userid, comments mapping"""
        mlist = []
        for k, v in self.answers.items():
            mapping = {}
            mapping['userid'] = k
            mapping['comments'] = v.get('comments', '')
            mlist.append(mapping)
        return mlist

    security.declareProtected(permissions.View, 'getAnswerOptionsWeights')
    def getAnswerOptionsWeights(self):
        """
        The accessor ensures that the number of answerOptionsWeights matches 
        the number of answerOptions. This accessor will be redundant when 
        answer options become objects.
        """
        # Sanitize weights 
        weights = []
        fld = self.getField('answerOptionsWeights')
        if fld is not None:
            for w in fld.get(self):
                try:
                    i = int(w)
                    weights.append(i)
                except:
                    weights.append(0)
                
        target_len = len(self.getAnswerOptions())
        len_weights = len(weights)
        
        if len_weights > target_len:
            return weights[:target_len]
        elif len_weights < target_len:
            # Pad with zero
            weights.extend([0 for i in range(0,target_len - len_weights)])
            return weights
        return weights

    def validate_answerOptionsWeights(self, value):
        # Length of value must match length of answerOptions.
        # Each element must be a valid integer.
        request = self.REQUEST
        if request.has_key('answerOptions'):
            target_len = len(request.get('answerOptions', []))
        else:
            target_len = len(self.getAnswerOptions())

        if len(value) != target_len:
            return "Please enter %s integer values" % target_len
        
        for v in value:
            try:
                i = int(v)
            except:
                return "%s is not a valid integer" % v

    security.declareProtected(permissions.View, 'getAnswerOptionsAsObjects')
    def getAnswerOptionsAsObjects(self):
        """
        Assemble answerOptions and answerOptionsWeights into a list
        of objects. When answers become objects we can adjust this 
        method and leave calling code intact.
        """
        if not hasattr(self, 'getAnswerOptions'):
            return []

        class AnswerOptionHelper(BaseObject):
            def __init__(self, answeroption, weight, parent):
                self.answeroption = answeroption                
                self.weight = weight
                self.parent = parent
            
            def __call__(self):
                return self.answeroption

            def getWeight(self):
                return self.weight
        
            def aq_parent(self):
                return self.parent
                
        ret = []
        n = 0
        weights = self.getAnswerOptionsWeights()
        for ao in self.getAnswerOptions():
            # Index and conversion errors should not be present thanks to 
            # validators.
            ob = AnswerOptionHelper(ao, int(weights[n]), self)
            ret.append(ob)
            n += 1 
            
        return ret
        
    security.declareProtected(permissions.View, 'getNumberOfRespondents')
    def getNumberOfRespondents(self):
        return len(self.answers.keys())
        
    security.declareProtected(permissions.View, 'getWeightFor')
    def getWeightFor(self, answerOption):
        return self.getAnswerOptionsWeights()[list(self.getAnswerOptions()).index(answerOption)]

    security.declareProtected(permissions.View, 'getDimensionsVocab')
    def getDimensionsVocab(self):
        """Return dimensions of parent"""
        parent = self.aq_parent
        while parent and (parent.portal_type != 'Survey'):
            parent = parent.aq_parent
        
        if parent.portal_type == 'Survey':
            return parent.getDimensions()
            
        return []

    security.declareProtected(permissions.View, 'getMaxWeight')
    def getMaxWeight(self):
        """
        If in future we want max weight to be user settable then 
        calling code already use this method as an 'accessor'
        """
        return max([int(w) for w in self.getAnswerOptionsWeights()])

InitializeClass(BaseQuestion)
