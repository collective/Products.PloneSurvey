from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.permissions import View

from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.interfaces.survey_question \
    import IPloneSurveyQuestion

from BaseQuestion import BaseQuestion
from schemata import SurveyMatrixQuestionSchema


class SurveyMatrixQuestion(BaseQuestion):
    """A question in a matrix within a survey"""
    schema = SurveyMatrixQuestionSchema
    portal_type = 'Survey Matrix Question'
    _at_rename_after_creation = True
    implements(IPloneSurveyQuestion)
    security = ClassSecurityInfo()

    @security.protected(View)
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
        if self.getRequired() and not value and not value == 0:
            return 1
        self.addAnswer(value)

    @security.protected(View)
    def getRequired(self):
        """Return 1 or 0 depending on if a null value exists"""
        return self.aq_parent.getRequired()

    @security.protected(View)
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
            if answer['value'] or answer['value'] >= 0:
                if isinstance(answer['value'],
                              str) or isinstance(answer['value'], int):
                    try:
                        aggregate_answers[str(answer['value'])] += 1
                    except KeyError:
                        aggregate_answers[str(answer['value'])] = 1
                else:
                    for value in answer['value']:
                        try:
                            aggregate_answers[value] += 1
                        except KeyError:
                            aggregate_answers[value] = 1
        return aggregate_answers

    @security.protected(View)
    def getPercentageAnswers(self):
        """Return a mapping of aggregrate answer values,
        suitable for a barchart"""
        max = 0
        aggregate_answers = self.getAggregateAnswers()
        for k, v in aggregate_answers.items():
            if v > max:
                max = v
        pct_aggregate_answers = {}
        for k, v in aggregate_answers.items():
            if v == 0:
                value = 0
            else:
                value = v / float(max)
            pct_aggregate_answers[k] = int(value * 100)
        return pct_aggregate_answers

    @security.protected(View)
    def getPercentages(self):
        """Return a mapping of percentages for each answer"""
        total = 0
        aggregate_answers = self.getAggregateAnswers()
        for k, v in aggregate_answers.items():
            total = v + total
        pct_answers = {}
        for k, v in aggregate_answers.items():
            if v == 0:
                value = 0
            else:
                value = v / float(total)
            pct_answers[k] = int(value * 100)
        return pct_answers

    @security.protected(View)
    def getAnswerOptionsWeights(self):
        return self.aq_parent.getAnswerOptionsWeights()

registerATCT(SurveyMatrixQuestion, PROJECTNAME)
