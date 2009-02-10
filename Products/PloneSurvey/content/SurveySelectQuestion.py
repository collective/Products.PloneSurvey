from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import SELECT_INPUT_TYPE, LIKERT_OPTIONS, LIKERT_OPTIONS_MAP
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema

MainSchema = BaseQuestionSchema.copy()
del MainSchema['required']

schema = MainSchema + Schema((

    IntegerField('likertOptions',
        searchable=0,
        required=0,
        vocabulary=LIKERT_OPTIONS,
        widget=SelectionWidget(
            label="Likert Options",
            label_msgid="XXX",
            description="Select a Likert scale to use for options, or use the box below.",
            description_msgid="XXX",
            i18n_domain="plonesurvey",
           ),
        ),

    BooleanField('reverseLikert',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Reverse Likert Scale",
            label_msgid="XXX",
            description="""Display the likert options in reverse order, bad to good.""",
            description_msgid="XXX",
            i18n_domain="plonesurvey",
          ),
        ),

    LinesField('answerOptions',
        searchable=0,
        required=0,
        default=("Yes", "No"),
        widget=LinesWidget(
            label="Answer options",
            label_msgid="label_answer_options",
            description="""Enter the options you want to be available to the user here.
                           Press enter to seperate the options.""",
            description_msgid="help_answer_options",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('nullValue',
        searchable=0,
        required=0,
        widget=StringWidget(
            label="Null Value",
            label_msgid="XXX",
            description="""Leave this blank to make the question required, or
                           enter a value for no response, eg Not applicable.
                           If this is a multiple select or checkbox field,
                           enter some random text, which will not appear in the survey,
                           to make this question not required.""",
            description_msgid="XXX",
            i18n_domain="plonesurvey",
           ),
        ),

##    LinesField('answerOptionsWeights',
##        searchable=0,
##        required=0,
##        default=("1", "-1"),
##        widget=LinesWidget(
##            label="Answer option weights",
##            label_msgid="label_answer_options_weights",
##            description="""Enter the weight for each answer option.
##                           Press enter to seperate the weights.""",
##            description_msgid="help_answer_options_weights",
##            i18n_domain="plonesurvey",
##           ),
##        ),

    StringField('inputType',
        searchable=0,
        required=0,
        vocabulary=SELECT_INPUT_TYPE,
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

class SurveySelectQuestion(BaseQuestion):
    """A question with select vocab within a survey"""
    schema = schema
    _at_rename_after_creation = True

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
                    state.setError(self.getId(), "This is not one of the answer options")
            else: # value is a list
                if self.getLikertOptions():
                    new_value = []
                    for item in value:
                        try:
                            item = int(item)
                        except ValueError:
                            state.setError(self.getId(), "This is not an integer")
                            return
                        else:
                            new_value.append(item)
                    value = new_value
                for item_value in value:
                    if not item_value in self.getQuestionOptions():
                        validates = False
                if not validates:
                        #state.setError(self.getId(), "This is not one of the answer options-2")
                        state.setError(self.getId(), str(value) + str(self.getQuestionOptions()))
                else:
                    self.addAnswer(value, comments)
        elif comments:
            # XXX something more intelligent needs to be done here, and if neither value or comments is
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
                vocab = vocab.sortedByKey()
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

registerType(SurveySelectQuestion)
