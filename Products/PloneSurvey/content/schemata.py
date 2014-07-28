# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import BooleanWidget
from Products.Archetypes.atapi import IntegerField
from Products.Archetypes.atapi import IntegerWidget
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import LinesWidget
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import TextField
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.lib.constraintypes \
    import ConstrainTypesMixinSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneSurvey import PloneSurveyMessageFactory as _
from Products.PloneSurvey.config import NOTIFICATION_METHOD
from Products.PloneSurvey.config import TEXT_INPUT_TYPE
from Products.PloneSurvey.config import SELECT_INPUT_TYPE
from Products.PloneSurvey.config import TEXT_LOCATION
from Products.PloneSurvey.config import COMMENT_TYPE
from Products.PloneSurvey.config import LIKERT_OPTIONS

SurveySchema = ATContentTypeSchema.copy() + ConstrainTypesMixinSchema + Schema((

    TextField(
        'body',
        searchable=1,
        required=0,
        schemata="Introduction",
        default_content_type='text/html',
        default_output_type='text/html',
        allowable_content_types=('text/plain',
                                 'text/structured',
                                 'text/html', ),
        widget=RichWidget(
            label=_('label_introduction',
                    default=u"Introduction"),
            description=_(
                'help_introduction',
                default=u"Enter an introduction for the survey."),
            rows=5,
        ),
    ),

    TextField(
        'thankYouMessage',
        required=0,
        searchable=0,
        default_method="translateThankYouMessage",
        widget=TextAreaWidget(
            label=_("label_thank",
                    default="'Thank you' message text"),
            description=_(
                'help_thankyou',
                default=u"This is the message that will be displayed to "
                        u"the user when they complete the survey."),
        ),
    ),

    TextField(
        'savedMessage',
        required=0,
        searchable=0,
        default_method="translateSavedMessage",
        widget=TextAreaWidget(
            label=_('label_saved_text',
                    default="'Saved' message text"),
            description=_(
                'help_saved_text',
                default=u"This is the message that will be displayed to the "
                        u"user when they save the survey, "
                        u"but don't submit it."),
        ),
    ),

    StringField(
        'exitUrl',
        required=0,
        searchable=0,
        widget=StringWidget(
            label=_("label_exit_url", default=u"Exit URL"),
            description=_(
                "help_exit_url",
                default=u'This is the URL that the user will be directed to '
                        u'on completion of the survey.\n'
                        u'Use "http://site.to.go.to/page" or "route/to/page" '
                        u'for this portal'),
        ),
    ),

    BooleanField(
        'confidential',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_(u"label_confidential", default=u"Confidential"),
            description=_(
                "help_confidential",
                default=u"Prevent respondents usernames from appearing in "
                        u"results"),
        ),
    ),

    BooleanField(
        'allowAnonymous',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_('label_allow_anonymous', default=u"Allow Anonymous"),
            description=_(
                'help_allow_anonymous',
                default=u"Anonymous user will be able to fill the survey"),
        ),
    ),

    BooleanField(
        'allowSave',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_("label_allow_save", default=u"Allow Save Functionality"),
            description=_(
                "help_allow_save",
                default=u"Allow logged in users to save survey for finishing "
                        u"later."),
        ),
    ),

    StringField(
        'surveyNotificationEmail',
        required=0,
        searchable=0,
        widget=StringWidget(
            label=_("label_survey_notification_email",
                    default=u"Survey Notification Email Address"),
            description=_(
                "help_survey_notification_email",
                default=u"Enter an email address to receive notifications of "
                        u"survey completions."),
        ),
    ),

    StringField(
        'surveyNotificationMethod',
        required=0,
        searchable=0,
        vocabulary=NOTIFICATION_METHOD,
        widget=SelectionWidget(
            label=_("label_survey_notification_method",
                    default=u"Survey Notification Method"),
            description=_(
                "help_survey_notification_method",
                default=u"Select a method to receive notification emails."),
        ),
    ),

    StringField(
        'completedFor',
        searchable=0,
        required=0,
        default=[],
        widget=StringWidget(visible=0,),
    ),

    BooleanField(
        'showCaptcha',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_("label_show_captcha", default=u"Show Captcha"),
        ),
    ),

    TextField(
        'emailInvite',
        searchable=1,
        required=0,
        schemata="Email Invite",
        default_method="_get_emailInvite_default",
        default_content_type='text/html',
        default_output_type='text/html',
        allowable_content_types=('text/plain',
                                 'text/structured',
                                 'text/html', ),
        widget=RichWidget(
            label=_('label_email_invite', default=u"Email Invite"),
            description=_(
                'help_email_invite',
                default=u"An email invite will be sent to loaded respondents, "
                        u"use '**Name**' for the respondents name, "
                        u"and '**Survey**' for the title of the survey as "
                        u"a link to the survey.", )
        ),
    ),

    StringField(
        'inviteFromName',
        schemata="Email Invite",
        required=0,
        searchable=0,
        widget=StringWidget(
            label=_("label_invite_from_name", default=u"Person Invite From"),
            description=_(
                "help_invite_from_name",
                default=u"Enter person's name that the survey invite email is "
                        u"from."),
        ),
    ),

    StringField(
        'inviteFromEmail',
        schemata="Email Invite",
        required=0,
        searchable=0,
        widget=StringWidget(
            label=_("label_invite_from_email", default=u"Email Invite From"),
            description=_(
                "help_invite_from_email",
                default=u"Enter person's email address that the survey invite "
                        u"email is from."
            ),
        ),
    ),

))

finalizeATCTSchema(SurveySchema, moveDiscussion=False)
SurveySchema["description"].widget.label = _("label_description",
                                             default=u"Survey description")
SurveySchema["description"].widget.description = _(
    "help_description",
    default=u"Add a short description of the survey here.")
del SurveySchema["relatedItems"]

SubSurveySchema = ATContentTypeSchema.copy() + Schema((

    StringField(
        'requiredQuestion',
        schemata="Branching",
        searchable=0,
        required=0,
        vocabulary='getValidationQuestions',
        widget=SelectionWidget(
            format="radio",
            label=_("label_previous_question",
                    default=u"Conditional Question"),
            description=_(
                "help_previous_question",
                default=u"The conditional question determines whether to "
                        u"display this Sub Survey. Select 'None' to display "
                        u"the Sub Survey unconditionally."),
        ),
    ),

    StringField(
        'requiredAnswer',
        schemata="Branching",
        searchable=0,
        required=0,
        vocabulary='getQuestions',
        widget=StringWidget(
            label=_("label_previous_question_answer",
                    default=u"Required Answer"),
            description=_(
                "help_previous_question_answer",
                default=u"Enter a required answer to the conditional question "
                        u"above to determine whether this Sub Survey is "
                        u"displayed."),
        ),
    ),

    BooleanField(
        'requiredAnswerYesNo',
        schemata="Branching",
        searchable=0,
        required=0,
        default=1,
        widget=BooleanWidget(
            label=_("label_previous_question_answer_yes_no",
                    default=u"Use Required Answer?"),
            description=_(
                "help_previous_question_answer_yes_no",
                default=u"Check this box if the required answer should be "
                        u"selected for this Sub Survey to be displayed."),
        ),
    ),

))

finalizeATCTSchema(SubSurveySchema, moveDiscussion=False)
SubSurveySchema["description"].widget.label = _("label_description",
                                                default=u"Survey description")
SubSurveySchema["description"].widget.description = _(
    "help_description",
    default=u"Add a short description of the survey here.")
del SubSurveySchema["relatedItems"]

BaseQuestionSchema = ATContentTypeSchema.copy() + Schema((

    BooleanField(
        'required',
        searchable=0,
        required=0,
        default=1,
        widget=BooleanWidget(
            label=_("label_required", default=u"Required"),
            description=_(
                "help_required",
                default=u"Select if this question is required, meaning "
                        u"participant must give a response."),
        ),
    ),

    StringField(
        'commentType',
        schemata="Comment Field",
        searchable=0,
        required=0,
        vocabulary=COMMENT_TYPE,
        widget=SelectionWidget(
            label=_("label_comment_type", default=u"Comment Type"),
            description=_(
                "help_label_comment_type",
                default=u"Select what type of comment box you would like."),
            format="select",
        )
    ),

    StringField(
        'commentLabel',
        schemata="Comment Field",
        searchable=0,
        required=0,
        default_method="_get_commentLabel_default",
        widget=StringWidget(
            label=_("label_comment_label", default=u"Comment label"),
            description=_("help_comment_label", default="The comment label."),
        )
    ),

    TextField(
        'body',
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
            label=_("label_textblockbody", default=u"Text Block"),
        ),
    ),

    IntegerField(
        'textLocation',
        schemata="Text Block",
        searchable=0,
        required=0,
        default=0,
        vocabulary=TEXT_LOCATION,
        widget=SelectionWidget(
            format="radio",
            label=_("label_textlocation", default=u"Location of Text Block"),
            description=_(
                "help_textlocation",
                default=u"Select where the text block above should appear."),
        ),
    ),

))

BaseQuestionSchema["title"].widget.label = "Question"
BaseQuestionSchema["description"].widget.label = _(
    "label_question_description",
    default=u"Description")
BaseQuestionSchema["description"].widget.description = _(
    "help_question_description",
    default=u"Add a long description of the question here, to clarify any "
            u"details.")

SurveyDateQuestionSchema = BaseQuestionSchema.copy() + Schema((

    BooleanField(
        'showYMD',
        storage=AnnotationStorage(),
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_("label_showymd",
                    default=u"Show date"),
        ),
    ),

    BooleanField(
        'showHM',
        storage=AnnotationStorage(),
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_("label_showhm",
                    default=u"Show hours and minutes"),
        ),
    ),

    IntegerField(
        'startingYear',
        storage=AnnotationStorage(),
        searchable=0,
        required=0,
        widget=IntegerWidget(
            label=_("label_startingyear",
                    default=u"Starting Year"),
        ),
    ),

    IntegerField(
        'endingYear',
        storage=AnnotationStorage(),
        searchable=0,
        required=0,
        widget=IntegerWidget(
            label=_("label_endingyear",
                    default=u"Ending Year"),
        ),
    ),

    IntegerField(
        'futureYears',
        storage=AnnotationStorage(),
        searchable=0,
        required=0,
        widget=IntegerWidget(
            label=_("label_futureyears",
                    default=u"Future Years"),
        ),
    ),

))

finalizeATCTSchema(SurveyDateQuestionSchema, moveDiscussion=False)
del SurveyDateQuestionSchema['commentType']
del SurveyDateQuestionSchema['commentLabel']
del SurveyDateQuestionSchema['relatedItems']

SurveyTextQuestionSchema = BaseQuestionSchema.copy() + Schema((

    StringField(
        'inputType',
        searchable=0,
        required=0,
        vocabulary=TEXT_INPUT_TYPE,
        default='text',
        widget=SelectionWidget(
            label=_("label_input_type", default=u"Input Type"),
            description=_(
                "help_input_type",
                default=u"Please select what type of input you would "
                        u"like to use for this question."),
        ),
    ),

    IntegerField(
        'maxLength',
        searchable=0,
        required=0,
        default=4000,
        widget=StringWidget(
            label=_("label_maxlength",
                    default=u"Maximum length of characters"),
            description=_(
                "help_maxlength",
                default=u"Enter the maximum number of characters a user can "
                        u"enter for this question"),
        ),
    ),

    IntegerField(
        'cols',
        searchable=0,
        required=0,
        default=20,
        widget=StringWidget(
            label=_("label_text_cols", default="Cols (width in characters)"),
            description=_(
                "help_text_cols",
                default=u"Enter a number of columns for this field "
                        u"(width of the field in the characters)"),
        ),
    ),

    IntegerField(
        'rows',
        searchable=0,
        required=0,
        default=6,
        widget=StringWidget(
            label=_("label_text_rows", default=u"Rows (number of lines)"),
            description=_(
                "help_text_rows",
                default=u"Enter a number of rows for this field. "
                        u"This value is applicable only in the Text Area "
                        u"input type"),
        ),
    ),

    StringField(
        'validation',
        searchable=0,
        required=0,
        default='None',
        vocabulary='getValidators',
        widget=SelectionWidget(
            label=_(u"label_validation", default=u"Validation"),
            description=_("help_validation",
                          default=u"Select a validation for this question"),
        ),
    ),

))

finalizeATCTSchema(SurveyTextQuestionSchema, moveDiscussion=False)
del SurveyTextQuestionSchema['commentType']
del SurveyTextQuestionSchema['commentLabel']
del SurveyTextQuestionSchema["relatedItems"]

SurveySelectQuestionSchema = BaseQuestionSchema.copy() + Schema((

    IntegerField(
        'likertOptions',
        searchable=0,
        required=0,
        vocabulary=LIKERT_OPTIONS,
        widget=SelectionWidget(
            label=_("label_likertoptions", default=u"Likert Options"),
            description=_(
                "help_likertoptions",
                default=u"Select a Likert scale to use for options, "
                        u"or use the box below."),
        ),
    ),

    BooleanField(
        'reverseLikert',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_("label_reverselikert", default=u"Reverse Likert Scale"),
            description=_(
                "help_reverselikert",
                default=u"Display the likert options in reverse order, "
                        u"bad to good."),
        ),
    ),

    LinesField(
        'answerOptions',
        searchable=0,
        required=0,
        default_method="_get_yes_no_default",
        widget=LinesWidget(
            label=_('label_answer_options', default=u"Answer options"),
            description=_(
                "help_answer_options",
                default=u"Enter the options you want to be available to the "
                        u"user here. Press enter to separate the options."),
        ),
    ),

    StringField(
        'nullValue',
        searchable=0,
        required=0,
        widget=StringWidget(
            label=_("label_nullvalue", default=u"Null Value"),
            description=_(
                "help_nullvalue_select",
                default=u"Leave this blank to make the question required, or "
                        u"enter a value for no response, eg Not applicable. "
                        u"If this is a multiple select or checkbox field, "
                        u"enter some random text, which will not appear in "
                        u"the survey, to make this question not required."),
        ),
    ),

    StringField(
        'inputType',
        searchable=0,
        required=0,
        vocabulary=SELECT_INPUT_TYPE,
        widget=SelectionWidget(
            label=_("label_input_type", default="Input Type"),
            description=_(
                "help_input_type",
                default=u"Please select what type of input you would like to "
                        u"use for this question."),
        ),
    ),

))

finalizeATCTSchema(SurveySelectQuestionSchema, moveDiscussion=False)
del SurveySelectQuestionSchema['required']
del SurveySelectQuestionSchema["relatedItems"]

SurveyMatrixSchema = BaseQuestionSchema.copy() + Schema((

    IntegerField(
        'likertOptions',
        searchable=0,
        required=0,
        vocabulary=LIKERT_OPTIONS,
        widget=SelectionWidget(
            label=_("label_likertoptions", default=u"Likert Options"),
            description=_(
                "help_likertoptions",
                default=u"Select a Likert scale to use for options, "
                        u"or use the box below."),
        ),
    ),

    BooleanField(
        'reverseLikert',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label=_("label_reverselikert", default=u"Reverse Likert Scale"),
            description=_(
                "help_reverselikert",
                default=u"Display the likert options in reverse order, "
                        u"bad to good."),
        ),
    ),

    LinesField(
        'answerOptions',
        searchable=0,
        required=1,
        default_method="_get_yes_no_default",
        widget=LinesWidget(
            label=_("label_answer_options", default=u"Answer options"),
            description=_(
                "help_answer_options",
                default=u"Enter the options you want to be available to the "
                        u"user here. "
                        u"Press enter to separate the options."),
        ),
    ),

    StringField(
        'nullValue',
        searchable=0,
        required=0,
        widget=StringWidget(
            label=_("label_nullvalue", default=u"Null Value"),
            description=_(
                "help_nullvalue",
                default=u"Leave this blank to make the question required, "
                        u"or enter a value for no response, "
                        u"eg Not applicable"),
        ),
    ),

    StringField(
        'inputType',
        searchable=0,
        required=0,
        vocabulary=SELECT_INPUT_TYPE,
        widget=SelectionWidget(
            label=_("label_input_type", default=u"Input Type"),
            description=_(
                "help_input_type",
                default=u"Please select what type of input you would "
                        u"like to use for this question."),
        ),
    ),

))

finalizeATCTSchema(SurveyMatrixSchema, moveDiscussion=False)
del SurveyMatrixSchema['required']
del SurveyMatrixSchema["relatedItems"]

SurveyMatrixQuestionSchema = BaseQuestionSchema.copy()

finalizeATCTSchema(SurveyMatrixQuestionSchema, moveDiscussion=False)
del SurveyMatrixQuestionSchema['commentType']
del SurveyMatrixQuestionSchema['commentLabel']
del SurveyMatrixQuestionSchema['required']
del SurveyMatrixQuestionSchema["relatedItems"]
