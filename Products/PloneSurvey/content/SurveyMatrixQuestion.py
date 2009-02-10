import string
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import SELECT_INPUT_TYPE, BARCHART_COLORS
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema

MainSchema = BaseQuestionSchema.copy()
del MainSchema['commentType']
del MainSchema['commentLabel']
del MainSchema['required']

schema = MainSchema

finalizeATCTSchema(schema, moveDiscussion=False)
del schema["relatedItems"]

class SurveyMatrixQuestion(BaseQuestion):
    """A question in a matrix within a survey"""
    schema = schema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'validateAnswer')
    def validateAnswer(self, value, state):
        """Validate the question"""
        try:
            value = int(value)
        except TypeError:
            # most probably we have multiple selects
            newvalue = []
            for number in value:
                try:
                    newvalue.append(int(number))
                except ValueError:
                    newvalue.append(number)
            value = newvalue
        except ValueError:
            pass
        if self.getRequired() and not value:
           return 1
        self.addAnswer(value)

    security.declareProtected(permissions.View, 'getRequired')
    def getRequired(self):
        """Return 1 or 0 depending on if a null value exists"""
        return self.aq_parent.getRequired()

    security.declareProtected(permissions.View, 'getAggregateAnswers')
    def getAggregateAnswers(self):
        """Return a mapping of aggregrate answer values,
        suitable for a histogram"""
        if self.getInputType() in ['area', 'text']:
            return {}
        aggregate_answers = {}
        options = self.getQuestionOptions()
        for option in options:
            aggregate_answers[option] = 0
        for k, answer in self.answers.items():
            if answer['value']:
                if isinstance(answer['value'], str) or isinstance(answer['value'], int):
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

    security.declareProtected(permissions.View, 'getPercentages')
    def getPercentages(self):
        """Return a mapping of percentages for each answer"""
        total = 0
        aggregate_answers = self.getAggregateAnswers()
        for k,v in aggregate_answers.items():
            total = v + total
        pct_answers = {}
        for k,v in aggregate_answers.items():
            if v == 0:
                value = 0
            else:
                value = v/float(total)
            pct_answers[k] = int(value * 100)
        return pct_answers

    security.declareProtected(permissions.View, 'getAnswerOptionsWeights')
    def getAnswerOptionsWeights(self):
        return self.aq_parent.getAnswerOptionsWeights()

registerType(SurveyMatrixQuestion)
