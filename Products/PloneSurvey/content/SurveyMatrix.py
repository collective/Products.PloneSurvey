from AccessControl import ClassSecurityInfo
from BTrees.OOBTree import OOBTree

from Products.Archetypes.atapi import IntDisplayList
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore import permissions
from Products.CMFPlone.utils import safe_unicode

from Products.PloneSurvey.config import LIKERT_OPTIONS_MAP
from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion

from schemata import SurveyMatrixSchema


class SurveyMatrix(ATCTOrderedFolder, BaseQuestion):
    """A matrix of questions within a survey"""
    schema = SurveyMatrixSchema
    portal_type = 'Survey Matrix'
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    # A matrix doesn't have answers of its own, but it needs to have an
    # 'answers' attribute so that it plays properly with getAnswerFor etc.
    answers = OOBTree()

    security.declareProtected(permissions.View, 'validateAnswer')

    def validateAnswer(self, form, state):
        """Validate the question"""
        matrix_questions = self.getQuestions()
        error_string = ''
        for matrix_q in matrix_questions:
            matrix_qid = str(self.getId()) + '-' + str(matrix_q.getId())
            value = form.get(matrix_qid, '')
            error_value = matrix_q.validateAnswer(value, state)
            if error_value:
                error_string = error_string + ' ' + \
                    str(matrix_q.title_or_id()) + ','
        if error_string != '':
            error_string = safe_unicode(error_string[:-1])
            error_msg = self.translate(
                default='Please provide an answer for the question',
                msgid='please_provide_answer_for',
                domain='plonesurvey')
            state.setError(self.getId(), "%s %s" % (error_msg, error_string))

    security.declarePublic('canSetDefaultPage')

    def canSetDefaultPage(self):
        """Doesn't make sense for surveys to allow alternate views"""
        return False

    security.declarePublic('canConstrainTypes')

    def canConstrainTypes(self):
        """Should not be able to add non survey types"""
        return False

    security.declareProtected(permissions.View, 'getRequired')

    def getRequired(self):
        """Return 1 or 0 depending on if a null value exists"""
        if self.getNullValue():
            return 0
        else:
            return 1

    security.declareProtected(permissions.View, 'getQuestionOptions')

    def getQuestionOptions(self):
        """Return the options for this question"""
        if self.getLikertOptions():
            vocab = LIKERT_OPTIONS_MAP[self.getLikertOptions()]
            vocab = vocab
            if self.getReverseLikert():
                vocab = vocab.sortedByKey()
            if self.getNullValue():
                options = IntDisplayList()
                for item in vocab:
                    options.add(item, vocab.getValue(item))
                options.add(0, self.getNullValue())
                return options
            return vocab
        return self.getAnswerOptions()

    security.declareProtected(permissions.View, 'getQuestions')

    def getQuestions(self):
        """Return the questions for this part of the survey"""
        questions = self.getFolderContents(
            contentFilter={'portal_type': ['Survey Matrix Question', ]},
            full_objects=True)
        return questions

registerATCT(SurveyMatrix, PROJECTNAME)
