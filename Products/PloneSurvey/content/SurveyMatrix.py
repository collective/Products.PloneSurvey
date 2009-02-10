import string
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import SELECT_INPUT_TYPE, LIKERT_OPTIONS, LIKERT_OPTIONS_MAP
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema

MainSchema = BaseQuestionSchema.copy()
del MainSchema['required']
##del MainSchema['dimensions']

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
        required=1,
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
                           enter a value for no response, eg Not applicable""",
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

class SurveyMatrix(ATCTOrderedFolder, BaseQuestion):
    """A matrix of questions within a survey"""
    schema = schema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    # A matrix doesn't have answers of its own, but it needs to have an
    # 'answers' attribute so that it plays properly with getAnswerFor etc.
    answers = {}

    security.declareProtected(permissions.View, 'validateAnswer')
    def validateAnswer(self, form, state):
        """Validate the question"""
        matrix_questions = self.getQuestions()
        error_string = ''
        for matrix_q in matrix_questions:
            matrix_qid = str(self.getId()) + '-' + str(matrix_q.getId())
            value = form.get(matrix_qid, '')
            error_value = matrix_q.validateAnswer(value,state)
            if error_value:
                error_string = error_string + ' ' + str(matrix_q.title_or_id()) + ','
        if error_string != '':
            error_string = error_string[:-1]
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
            contentFilter={'portal_type':[
                'Survey Matrix Question',
                ]},
            full_objects=True)
        return questions

registerType(SurveyMatrix)
