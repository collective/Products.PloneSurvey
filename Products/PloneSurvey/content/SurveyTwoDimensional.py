import string
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import TWO_D_INPUT_TYPE
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema
from Products.PloneSurvey.content.SurveyTwoDimensionalQuestion import SurveyTwoDimensionalQuestion

MainSchema = BaseQuestionSchema.copy()

schema = MainSchema + Schema((

    StringField('inputType',
        searchable=0,
        required=0,
        vocabulary=TWO_D_INPUT_TYPE,
        default='radio',
        widget=SelectionWidget(
            label="Input Type",
            label_msgid="label_input_type",
            description="Please select what type of input you would like to use for this question.",
            description_msgid="help_input_type",
            i18n_domain="plonesurvey",
           ),
        ),

    ))

finalizeATCTSchema(schema, moveDiscussion=False)
del schema["relatedItems"]

class SurveyTwoDimensional(OrderedBaseFolder, BaseQuestion):
    """A two-dimensional question within a survey"""
    schema = schema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    # A 2D doesn't have answers of its own, but it needs to have an
    # 'answers' attribute so that it plays properly with getAnswerFor etc.
    answers = {}

    security.declareProtected(permissions.View, 'getAbstract')
    def getAbstract(self, **kw):
        return self.Description()

    security.declareProtected(permissions.ModifyPortalContent, 'setAbstract')
    def setAbstract(self, val, **kw):
        self.setDescription(val)
   
    security.declareProtected(permissions.View, 'getQuestions')
    def getQuestions(self):
        """Return the questions for this part of the survey"""
        questions = self.getFolderContents(
            contentFilter={'portal_type':[
                'Survey 2-Dimensional Question',
                ]},
            full_objects=True)
        return questions
        
    def at_post_create_script(self):
        """Create two Survey Select Questions"""
        # We can't use invokeFactory here because allowed_content_types is empty
        id1 = self.getId()+'-dimension-one'
        question = SurveyTwoDimensionalQuestion(id1)
        self._setObject(id1, question)
        question = self._getOb(id1)
        question.edit(title=self.title_or_id() + ' Dimension One')
        
        id2 = self.getId()+'-dimension-two'
        question = SurveyTwoDimensionalQuestion(id2)
        self._setObject(id2, question)
        question = self._getOb(id2)
        question.edit(title=self.title_or_id() + ' Dimension Two')

registerType(SurveyTwoDimensional)
