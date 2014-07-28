from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.Archetypes.atapi import IntDisplayList
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore import permissions

from Products.PloneSurvey.config import LIKERT_OPTIONS_MAP
from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.interfaces.survey_question \
    import IPloneSurveyQuestion

from BaseQuestion import BaseQuestion
from schemata import SurveySelectQuestionSchema


class SurveySelectQuestion(BaseQuestion):
    """A question with select vocab within a survey"""
    schema = SurveySelectQuestionSchema
    portal_type = 'Survey Select Question'
    _at_rename_after_creation = True

    implements(IPloneSurveyQuestion)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'validateAnswer')

    def validateAnswer(self, value, comments, state):
        """Validate the question"""
        validates = True
        if value:
            if hasattr(value, 'lower'):
                if self.getLikertOptions():
                    try:
                        value = int(value)
                    except ValueError:
                        state.setError(self.getId(), "This is not an integer")
                        return
                if value in self.getQuestionOptions():
                    self.addAnswer(value, comments)
                else:
                    state.setError(self.getId(),
                                   "This is not one of the answer options")
            else:  # value is a list
                if self.getLikertOptions():
                    new_value = []
                    for item in value:
                        try:
                            item = int(item)
                        except ValueError:
                            state.setError(self.getId(),
                                           "This is not an integer")
                            return
                        else:
                            new_value.append(item)
                    value = new_value
                for item_value in value:
                    if item_value not in self.getQuestionOptions():
                        validates = False
                if not validates:
                        state.setError(
                            self.getId(),
                            str(value) + str(self.getQuestionOptions()))
                else:
                    self.addAnswer(value, comments)
        elif comments:
            # XXX something more intelligent needs to be done here,
            # and if neither value or comments is
            # provided, then None is stored instead of empty string
            self.addAnswer(value, comments)

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
                vocab = IntDisplayList(sorted(vocab.items()))
            if self.getNullValue():
                options = IntDisplayList()
                for item in vocab:
                    options.add(item, vocab.getValue(item))
                options.add(0, self.getNullValue())
                return options
            return vocab
        return self.getAnswerOptions()

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
            if answer['value'] or answer['value'] >= 0:
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
        for k, v in aggregate_answers.items():
            if v > max:
                max = v
        pct_aggregate_answers = {}
        for k, v in aggregate_answers.items():
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
        for k, v in aggregate_answers.items():
            total = v + total
        pct_answers = {}
        for k, v in aggregate_answers.items():
            if v == 0:
                value = 0
            else:
                value = v/float(total)
            pct_answers[k] = int(value * 100)
        return pct_answers

registerATCT(SurveySelectQuestion, PROJECTNAME)
