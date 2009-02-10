from AccessControl import ClassSecurityInfo
#from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.validation import validation

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import TEXT_INPUT_TYPE, TEXT_VALIDATORS
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion, BaseQuestionSchema
#from Products.PloneSurvey.interfaces import ISurveyTextQuestion

MainSchema = BaseQuestionSchema.copy()
del MainSchema['commentType']
del MainSchema['commentLabel']

schema = MainSchema + Schema((

    StringField('inputType',
        searchable=0,
        required=0,
        vocabulary=TEXT_INPUT_TYPE,
        default='text',
        widget=SelectionWidget(
            label="Input Type",
            label_msgid="label_input_type",
            description="Please select what type of input you would like to use for this question.",
            description_msgid="help_input_type",
            i18n_domain="plonesurvey",
           ),
        ),

    IntegerField('maxLength',
        searchable=0,
        required=0,
        default=4000,
        widget=StringWidget(
            label="Maximum length of characters",
            label_msgid="XXX",
            description="Enter the maximum number of characters a user can enter for this question",
            description_msgid="XXX",
            i18n_domain="plonesurvey",
             ),
        ),

    IntegerField('cols',
        searchable=0,
        required=0,
        default=20,
        widget=StringWidget(
            label="Cols (width in characters)",
            label_msgid="label_text_cols",
            description="Enter a number of columns for this field (width of the field in the characters)",
            description_msgid="help_text_cols",
            i18n_domain="plonesurvey",
             ),
        ),

    IntegerField('rows',
        searchable=0,
        required=0,
        default=6,
        widget=StringWidget(
            label="Rows (number of lines)",
            label_msgid="label_text_rows",
            description="Enter a number of rows for this field. This value is applicable only in the Text Area input type",
            description_msgid="help_text_rows",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('validation',
        searchable=0,
        required=0,
        vocabulary='getValidators',
        widget=SelectionWidget(
            label="Validation",
            label_msgid="label_validation",
            description="Select a validation for this question",
            description_msgid="help_validation",
            i18n_domain="plonesurvey",
          ),
        ),

    ))

finalizeATCTSchema(schema, moveDiscussion=False)
del schema["relatedItems"]

class SurveyTextQuestion(BaseQuestion):
    """A textual question within a survey"""
    schema = schema
    _at_rename_after_creation = True

    #implements(ISurveyTextQuestion)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'getValidators')
    def getValidators(self):
        """Return a list of validators"""
        validator_list = ['None', ]
        validator_list.extend(TEXT_VALIDATORS)
        return validator_list

    security.declareProtected(permissions.View, 'getValidators')
    def validateQuestion(self, value):
        """Return a list of validators"""
        validator = self.getValidation()
        v = validation.validatorFor(validator)
        return v(value)

registerType(SurveyTextQuestion)
