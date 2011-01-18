# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneSurvey import PloneSurveyMessageFactory as _
from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import *
from Products.PloneSurvey.config import DEFAULT_SURVEY_INVITE

SurveySchema = ATContentTypeSchema.copy() + ConstrainTypesMixinSchema + Schema((
    
    TextField('body',
        searchable = 1,
        required=0,
        schemata="Introduction",
        default_content_type    = 'text/html',
        default_output_type     = 'text/html',
        allowable_content_types=('text/plain',
                                 'text/structured',
                                 'text/html',
                                ),
        widget = RichWidget(label = _('label_introduction',
                                      default=u"Introduction"),
                            description = _('help_introduction',
                                            default=u"Enter an introduction for the survey."),
                            rows = 5,
                           ),
        ),

##    LinesField('dimensions',
##        searchable=0,
##        required=0,
##        default=[],
##        widget=LinesWidget(
##            label="Dimensions",
##            label_msgid="label_dimensions",
##            description="""Questions can be associated with one or more dimensions.
##                           Press enter to seperate the options.""",
##            description_msgid="help_dimensions",
##            i18n_domain="plonesurvey",),
##        ),

    TextField('thankYouMessage',
        required=0,
        searchable=0,
        default_method="translateThankYouMessage",
        widget=TextAreaWidget(
            label=_("label_thank",
                    default="'Thank you' message text"),
            description=_('help_thankyou',
                          default=u"This is the message that will be displayed to the "
                                  u"user when they complete the survey."),
           ),
        ),

    TextField('savedMessage',
        required=0,
        searchable=0,
        default_method="translateSavedMessage",
        widget=TextAreaWidget(
            label=_('label_saved_text',
                    default="'Saved' message text"),
            description=_('help_saved_text',
                          default=u"This is the message that will be displayed to the user "
                                  u"when they save the survey, but don't submit it."),
           ),
        ),

    StringField('exitUrl',
        required=0,
        searchable=0,
        widget=StringWidget(
            label=_("label_exit_url", default=u"Exit URL"),
            description=_("help_exit_url",
                          default=u'This is the URL that the user will be directed to on '
                                  u'completion of the survey.\n'
                                  u'Use "http://site.to.go.to/page" or "route/to/page" '
                                  u'for this portal'),
          ),
        ),

    BooleanField('confidential',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_(u"label_confidential", default=u"Confidential"),
            description=_("help_confidential",
                          default=u"Prevent respondents usernames from appearing in results"),
          ),
        ),

    BooleanField('allowAnonymous',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Allow Anonymous",
            label_msgid="label_allow_anonymous",
            i18n_domain="plonesurvey",
          ),
        ),

    BooleanField('allowSave',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Allow Save Functionality",
            label_msgid="label_allow_save",
            description="Allow logged in users to save survey for finishing later.",
            description_msgid="help_allow_save",
            i18n_domain="plonesurvey",
          ),
        ),

    StringField('surveyNotificationEmail',
        required=0,
        searchable=0,
        widget=StringWidget(
            label="Survey Notification Email Address",
            label_msgid="label_survey_notification_email",
            description="Enter an email address to receive notifications of survey completions.",
            description_msgid="help_survey_notification_email",
            i18n_domain="plonesurvey",
          ),
        ),

    StringField('surveyNotificationMethod',
        required=0,
        searchable=0,
        vocabulary=NOTIFICATION_METHOD,
        widget=SelectionWidget(
            label="Survey Notification Method",
            label_msgid="label_survey_notification_method",
            description="Select a method to receive notification emails.",
            description_msgid="help_survey_notification_method",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('completedFor',
        searchable=0,
        required=0,
        default=[],
        widget=StringWidget(visible=0,),
        ),

    BooleanField('showCaptcha',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Show Captcha",
            label_msgid="label_show_captcha",
            i18n_domain="plonesurvey",
          ),
        ),

    TextField('emailInvite',
        searchable = 1,
        required = 0,
        schemata = "Email Invite",
        default = DEFAULT_SURVEY_INVITE,
        default_content_type    = 'text/html',
        default_output_type     = 'text/html',
        allowable_content_types=('text/plain',
                                 'text/structured',
                                 'text/html',
                                ),
        widget = RichWidget(description = """An email invite will be sent to loaded respondents,
                                             use '**Name**' for the respondents name,
                                             and '**Survey**' for the title of the survey as a link to the survey.""",
                            label = "Email Invite",
                            label_msgid = 'label_email_invite',
                            description_msgid = 'help_email_invite',
                            rows = 5,
                            i18n_domain = "plonesurvey",
                           ),
    ),

    StringField('inviteFromName',
        schemata = "Email Invite",
        required=0,
        searchable=0,
        widget=StringWidget(
            label="Person Invite From",
            label_msgid="label_invite_from_name",
            description="Enter person's name that the survey invite email is from.",
            description_msgid="help_invite_from_name",
            i18n_domain="plonesurvey",
          ),
        ),

    StringField('inviteFromEmail',
        schemata = "Email Invite",
        required=0,
        searchable=0,
        widget=StringWidget(
            label="Email Invite From",
            label_msgid="label_invite_from_email",
            description="Enter person's email address that the survey invite email is from.",
            description_msgid="help_invite_from_email",
            i18n_domain="plonesurvey",
          ),
        ),

))

finalizeATCTSchema(SurveySchema, moveDiscussion=False)
SurveySchema["description"].widget.label = "Survey description"
SurveySchema["description"].widget.label_msgid = "label_description"
SurveySchema["description"].widget.description = "Add a short description of the survey here."
SurveySchema["description"].widget.description_msgid = "help_description"
SurveySchema["description"].widget.i18n_domain = "plonesurvey"
del SurveySchema["relatedItems"]

SubSurveySchema = ATContentTypeSchema.copy() + Schema((

    StringField('requiredQuestion',
        schemata="Branching",
        searchable=0,
        required=0,
        vocabulary='getValidationQuestions',
        widget=SelectionWidget(
            format="radio",
            label="Conditional Question",
            label_msgid="label_previous_question",
            description="""The conditional question determines whether to display this Sub Survey.
            Select 'None' to display the Sub Survey unconditionally.""",
            description_msgid="help_previous_question",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('requiredAnswer',
        schemata="Branching",
        searchable=0,
        required=0,
        vocabulary='getQuestions',
        widget=StringWidget(
            label="Required Answer",
            label_msgid="label_previous_question_answer",
            description="""Enter a required answer to the conditional question above to determine
            whether this Sub Survey is displayed.""",
            description_msgid="help_previous_question_answer",
            i18n_domain="plonesurvey",
          ),
        ),

    BooleanField('requiredAnswerYesNo',
        schemata="Branching",
        searchable=0,
        required=0,
        default=1,
        widget=BooleanWidget(
            label="Use Required Answer?",
            label_msgid="label_previous_question_answer_yes_no",
            description="Check this box if the required answer should be selected for this Sub Survey to be displayed.",
            description_msgid="help_previous_question_answer_yes_no",
            i18n_domain="plonesurvey",
          ),
        ),

    ))

finalizeATCTSchema(SubSurveySchema, moveDiscussion=False)
SubSurveySchema["description"].widget.label = "Survey description"
SubSurveySchema["description"].widget.label_msgid = "label_description"
SubSurveySchema["description"].widget.description = "Add a short description of the survey here."
SubSurveySchema["description"].widget.description_msgid = "help_description"
SubSurveySchema["description"].widget.i18n_domain = "plonesurvey"
del SubSurveySchema["relatedItems"]

BaseQuestionSchema = ATContentTypeSchema.copy() + Schema((

    BooleanField('required',
        searchable=0,
        required=0,
        default=1,
        widget=BooleanWidget(
            label="Required",
            label_msgid="label_required",
            description="Select if this question is required, meaning participant must give a response.",
            description_msgid="help_required",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('commentType',
        schemata="Comment Field",
        searchable=0,
        required=0,
        vocabulary=COMMENT_TYPE,
        widget=SelectionWidget(
            label="Comment Type",
            label_msgid="label_comment_type",
            description="Select what type of comment box you would like.",
            description_msgid="help_label_comment_type",
            format="select",
            i18n_domain="plonesurvey",
          )
        ),

    StringField('commentLabel',
        schemata="Comment Field",
        searchable=0,
        required=0,
        default="Comment - mandatory if \"no\"",
        widget=StringWidget(
            label="Comment label",
            label_msgid="label_comment_label",
            description="The comment label.",
            description_msgid="help_comment_label",
            i18n_domain="plonesurvey",
          )
        ),

    TextField('body',
        schemata="Text Block",
        searchable=0,
        required=0,
        default_content_type='text/html',
        default_output_type='text/x-html-safe',
        allowable_content_types=('text/structured',
                                 'text/restructured',
                                 'text/html',
                                 'text/plain',),
        widget=RichWidget(
            label="Text Block",
            label_msgid="label_textblockbody",
            i18n_domain="plonesurvey",
           ),
        ),

    IntegerField('textLocation',
        schemata="Text Block",
        searchable=0,
        required=0,
        default=0,
        vocabulary=TEXT_LOCATION,
        widget=SelectionWidget(
            format="radio",
            label="Location of Text Block",
            label_msgid="label_textlocation",
            description="Select where the text block above should appear.",
            description_msgid="help_textlocation",
            i18n_domain="plonesurvey",
           ),
        ),

##    LinesField('dimensions',
##        searchable=0,
##        required=0,
##        default=[],
##        multiValued=1,
##        vocabulary='getDimensionsVocab',
##        widget=MultiSelectionWidget(
##            format='checkbox',
##            label="Dimensions",
##            label_msgid="label_dimensions",
##            description="""Specify the dimensions which apply to this question.""",
##            description_msgid="help_dimensions",
##            i18n_domain="plonesurvey",),
##        index='FieldIndex'
##        ),

    ))

BaseQuestionSchema["title"].widget.label = "Question"
BaseQuestionSchema["description"].widget.label = "Description"
BaseQuestionSchema["description"].widget.label_msgid = "label_question_description"
BaseQuestionSchema["description"].widget.description = "Add a long description of the question here, to clarify any details."
BaseQuestionSchema["description"].widget.description_msgid = "help_question_description"
BaseQuestionSchema["description"].widget.i18n_domain = "plonesurvey"

SurveyDateQuestionSchema = BaseQuestionSchema.copy() + Schema((

    BooleanField('showYMD',
        storage = AnnotationStorage(),
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Show date",
            label_msgid="label_showymd",
            description="",
            description_msgid="help_showymd",
            i18n_domain="plonesurvey",
        ),
    ),

    BooleanField('showHM',
        storage = AnnotationStorage(),
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Show hours and minutes",
            label_msgid="label_showhm",
            description="",
            description_msgid="help_showhmd",
            i18n_domain="plonesurvey",
        ),
    ),

    IntegerField('startingYear',
        storage = AnnotationStorage(),
        searchable=0,
        required=0,
        widget=IntegerWidget(
            label="Starting Year",
            label_msgid="label_startingyear",
            description="",
            description_msgid="help_startingyear",
            i18n_domain="plonesurvey",
        ),
    ),

    IntegerField('endingYear',
        storage = AnnotationStorage(),
        searchable=0,
        required=0,
        widget=IntegerWidget(
            label="Ending Year",
            label_msgid="label_endingyear",
            description="",
            description_msgid="help_endingyear",
            i18n_domain="plonesurvey",
        ),
    ),

    IntegerField('futureYears',
        storage = AnnotationStorage(),
        searchable=0,
        required=0,
        widget=IntegerWidget(
            label="Future Years",
            label_msgid="label_futureyears",
            description="",
            description_msgid="help_futureyears",
            i18n_domain="plonesurvey",
        ),
    ),

))

finalizeATCTSchema(SurveyDateQuestionSchema, moveDiscussion=False)
del SurveyDateQuestionSchema['commentType']
del SurveyDateQuestionSchema['commentLabel']
del SurveyDateQuestionSchema["relatedItems"]

SurveyTextQuestionSchema = BaseQuestionSchema.copy() + Schema((

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
            label_msgid="label_maxlength",
            description="Enter the maximum number of characters a user can enter for this question",
            description_msgid="help_maxlength",
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
        default = 'None',
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

finalizeATCTSchema(SurveyTextQuestionSchema, moveDiscussion=False)
del SurveyTextQuestionSchema['commentType']
del SurveyTextQuestionSchema['commentLabel']
del SurveyTextQuestionSchema["relatedItems"]

SurveySelectQuestionSchema = BaseQuestionSchema.copy() + Schema((

    IntegerField('likertOptions',
        searchable=0,
        required=0,
        vocabulary=LIKERT_OPTIONS,
        widget=SelectionWidget(
            label="Likert Options",
            label_msgid="label_likertoptions",
            description="Select a Likert scale to use for options, or use the box below.",
            description_msgid="help_likertoptions",
            i18n_domain="plonesurvey",
           ),
        ),

    BooleanField('reverseLikert',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Reverse Likert Scale",
            label_msgid="label_reverselikert",
            description="""Display the likert options in reverse order, bad to good.""",
            description_msgid="help_reverselikert",
            i18n_domain="plonesurvey",
          ),
        ),

    LinesField('answerOptions',
        searchable=0,
        required=0,
        default_method="_get_yes_no_default",
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
            label_msgid="label_nullvalue",
            description="""Leave this blank to make the question required, or
                           enter a value for no response, eg Not applicable.
                           If this is a multiple select or checkbox field,
                           enter some random text, which will not appear in the survey,
                           to make this question not required.""",
            description_msgid="help_nullvalue",
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

finalizeATCTSchema(SurveySelectQuestionSchema, moveDiscussion=False)
del SurveySelectQuestionSchema['required']
del SurveySelectQuestionSchema["relatedItems"]

SurveyMatrixSchema = BaseQuestionSchema.copy() + Schema((

    IntegerField('likertOptions',
        searchable=0,
        required=0,
        vocabulary=LIKERT_OPTIONS,
        widget=SelectionWidget(
            label="Likert Options",
            label_msgid="label_likertoptions",
            description="Select a Likert scale to use for options, or use the box below.",
            description_msgid="help_likertoptions",
            i18n_domain="plonesurvey",
           ),
        ),

    BooleanField('reverseLikert',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Reverse Likert Scale",
            label_msgid="label_reverselikert",
            description="""Display the likert options in reverse order, bad to good.""",
            description_msgid="help_reverselikert",
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
            label_msgid="label_nullvalue",
            description="""Leave this blank to make the question required, or
                           enter a value for no response, eg Not applicable""",
            description_msgid="help_nullvalue",
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

finalizeATCTSchema(SurveyMatrixSchema, moveDiscussion=False)
del SurveyMatrixSchema['required']
##del SurveyMatrixSchema['dimensions']
del SurveyMatrixSchema["relatedItems"]

SurveyMatrixQuestionSchema = BaseQuestionSchema.copy()

finalizeATCTSchema(SurveyMatrixQuestionSchema, moveDiscussion=False)
del SurveyMatrixQuestionSchema['commentType']
del SurveyMatrixQuestionSchema['commentLabel']
del SurveyMatrixQuestionSchema['required']
del SurveyMatrixQuestionSchema["relatedItems"]

SurveyTwoDimensionalSchema = BaseQuestionSchema.copy() + Schema((

    StringField('inputType',
        searchable=0,
        required=0,
        vocabulary=TWO_D_INPUT_TYPE,
        default='radio',
        widget=SelectionWidget(
            label="Input Type",
            label_msgid="label_input_type",
            description="Please select what type of input you would like to use for this question.",
            description_msgid="help_input_type",
            i18n_domain="plonesurvey",
           ),
        ),

))

finalizeATCTSchema(SurveyTwoDimensionalSchema, moveDiscussion=False)
del SurveyTwoDimensionalSchema["relatedItems"]

SurveyTwoDimensionalQuestionSchema = BaseQuestionSchema.copy() + Schema((

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

finalizeATCTSchema(SurveyTwoDimensionalQuestionSchema, moveDiscussion=False)
del SurveyTwoDimensionalQuestionSchema['required']
##SurveyTwoDimensionalQuestionSchema['dimensions'].widget.visible = {'view':'visible', 'edit':'invisible'}
del SurveyTwoDimensionalQuestionSchema["relatedItems"]
