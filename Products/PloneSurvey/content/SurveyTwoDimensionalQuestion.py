from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import registerATCT

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import PROJECTNAME

from BaseQuestion import BaseQuestion
from schemata import SurveyTwoDimensionalQuestionSchema

class SurveyTwoDimensionalQuestion(BaseQuestion):
    """A two-dimensional question with a weighted vocab within a survey"""
    schema = SurveyTwoDimensionalQuestionSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'getRequired')
    def getRequired(self):
        """Use parent's value"""
        return self.aq_parent.getRequired()

    security.declareProtected(permissions.View, 'getInputType')
    def getInputType(self):
        """Use parent's value"""
        return self.aq_parent.getInputType()

    security.declareProtected(permissions.View, 'getDimensions')
    def getDimensions(self):
        """Use parent's value"""
        return self.aq_parent.getDimensions()

    security.declareProtected(permissions.View, 'getQuestionOptions')
    def getQuestionOptions(self):
        """Return the options for this question"""
        return self.getAnswerOptions()

    security.declareProtected(permissions.View, 'getAggregateAnswers')
    def getAggregateAnswers(self):
        """Return a mapping of aggregrate answer values,
        suitable for a histogram"""
        if self.getInputType() in ['area', 'text']:
            return {}
        aggregate_answers = {}
        options = self.getAnswerOptions()
        for option in options:
            aggregate_answers[option] = 0
        for k, answer in self.answers.items():
            if answer['value'] or answer['value'] >= 0:
                if isinstance(answer['value'], str):
                    try:
                        aggregate_answers[answer['value']] += 1
                    except KeyError:
                        aggregate_answers[answer['value']] = 1
                else:
                    for value in answer['value']:
                        try:
                            aggregate_answers[value] += 1
                        except KeyError:
                            aggregate_answers[value] = 1
        return aggregate_answers

    security.declareProtected(permissions.View, 'getPercentageAnswers')
    def getPercentageAnswers(self):
        """Return a mapping of aggregrate answer values,
        suitable for a barchart"""
        max = 0
        aggregate_answers = self.getAggregateAnswers()
        for k,v in aggregate_answers.items():
            if v > max:
                max = v
        pct_aggregate_answers = {}
        for k,v in aggregate_answers.items():
            if v == 0:
                value = 0
            else:
                value = v/float(max)
            pct_aggregate_answers[k] = int(value * 100)
        return pct_aggregate_answers

registerATCT(SurveyTwoDimensionalQuestion, PROJECTNAME)
