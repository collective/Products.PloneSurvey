import string
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import PROJECTNAME

from BaseQuestion import BaseQuestion
from SurveyTwoDimensionalQuestion import SurveyTwoDimensionalQuestion
from schemata import SurveyTwoDimensionalSchema

class SurveyTwoDimensional(OrderedBaseFolder, BaseQuestion):
    """A two-dimensional question within a survey"""
    schema = SurveyTwoDimensionalSchema
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

registerATCT(SurveyTwoDimensional, PROJECTNAME)
