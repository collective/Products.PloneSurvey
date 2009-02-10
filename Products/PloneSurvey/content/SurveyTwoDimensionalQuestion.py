from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import TWO_D_INPUT_TYPE
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema

MainSchema = BaseQuestionSchema.copy()
del MainSchema['required']
##MainSchema['dimensions'].widget.visible = {'view':'visible', 'edit':'invisible'}

schema = MainSchema + Schema((

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
   
    ))

finalizeATCTSchema(schema, moveDiscussion=False)
del schema["relatedItems"]

class SurveyTwoDimensionalQuestion(BaseQuestion):
    """A two-dimensional question with a weighted vocab within a survey"""
    schema = schema
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
            if answer['value']:
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
        
registerType(SurveyTwoDimensionalQuestion)
