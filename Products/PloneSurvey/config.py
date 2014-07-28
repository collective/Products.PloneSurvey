PROJECTNAME = "Products.PloneSurvey"

from Products.Archetypes.utils import DisplayList
from Products.Archetypes.utils import IntDisplayList
from Products.validation import validation

from Products.PloneSurvey import PloneSurveyMessageFactory as _

SKINS_DIR = 'skins'

GLOBALS = globals()

DEFAULT_SURVEY_INVITE = u'''
<p>Dear **Name**,</p>
<p>Please complete the **Survey**</p>
<p>Thank you</p>'''

NOTIFICATION_METHOD = DisplayList((
    ('', _(u'label_no_emails', default=u'No emails')),
    ('each_submission', _(u'label_all_emails',
                          default=u'Email on each submission')),
    ))

TEXT_INPUT_TYPE = DisplayList((
    ('text', _(u'label_text_field', default=u'Text Field')),
    ('area', _(u'label_text_area', default=u'Text Area')),
    ))

SELECT_INPUT_TYPE = DisplayList((
    ('radio', _(u'label_radio_buttons', default=u'Radio Buttons')),
    ('selectionBox', _(u'label_selection_box', default=u'Selection Box')),
    ('multipleSelect', _(u'label_multiple_selection_box',
                         default=u'Multiple Selection Box')),
    ('checkbox', _(u'label_check_boxes', default=u'Check Boxes')),
    ))

TEXT_LOCATION = IntDisplayList((
    (0, _(u'label_does_not_appear', default=u'Does not appear')),
    (1, _(u'label_appears_above_question', default=u'Appears above question')),
    (2, _(u'label_appears_between_question_and_answer',
          default=u'Appears between question and answer')),
    (3, _(u'label_appears_after_answer', default=u'Appears after answer')),
    ))

COMMENT_TYPE = DisplayList((
    ('', _(u'label_no_comment_field', default=u'None')),
    ('text', _(u'label_text_field', default=u'Text Field')),
    ('area', _(u'label_text_area', default=u'Text Area')),
    ))

LIKERT_OPTIONS = IntDisplayList((
    (0, _(u'label_use_options_below', default=u'Use the options below')),
    (1, _(u'list_good_poor',
          default=u'("Very Good", "Good", "OK Only", "Poor", "Very Poor")')),
    (2, _(u'list_useful_notuseful',
          default=u'("Very Useful", "Useful", "Quite Useful", "A little Useful", "Not Useful")')),
    (3, _(u'list_agree_disagree', default=u'("Agree Strongly", "Agree", "Neutral", "Disagree", "Disagree Strongly")')),
    ))

LIKERT_OPTIONS_MAP = {
    1: IntDisplayList((
        (5, _(u'Very Good', default=u'Very Good')),
        (4, _(u'Good', default=u'Good')),
        (3, _(u'OK Only', default=u'OK Only')),
        (2, _(u'Poor', default=u'Poor')),
        (1, _(u'Very Poor', default=u'Very Poor')),
        )),
    2: IntDisplayList((
        (5, _(u'Very Useful', default=u'Very Useful')),
        (4, _(u'Useful', default=u'Useful')),
        (3, _(u'Quite Useful', default=u'Quite Useful')),
        (2, _(u'A little Useful', default=u'A little Useful')),
        (1, _(u'Not Useful', default=u'Not Useful')),
        )),
    3: IntDisplayList((
        (5, _(u'Agree Strongly', default=u'Agree Strongly')),
        (4, _(u'Agree', default=u'Agree')),
        (3, _(u'Neutral', default=u'Neutral')),
        (2, _(u'Disagree', default=u'Disagree')),
        (1, _(u'Disagree Strongly', default=u'Disagree Strongly')),
        )),
    }

BARCHART_COLORS = ['barchart_blue.gif',
                   'barchart_green.gif',
                   'barchart_red.gif',
                   'barchart_yellow.gif',
                   'barchart_cyan.gif',
                   'barchart_magneta.gif']

VALIDATORS = validation.keys()

# remove non useful validators
if 'isEmpty' in VALIDATORS:
    VALIDATORS.remove('isEmpty')
if 'isValidId' in VALIDATORS:
    VALIDATORS.remove('isValidId')
if 'checkImageMaxSize' in VALIDATORS:
    VALIDATORS.remove('checkImageMaxSize')
if 'checkNewsImageMaxSize' in VALIDATORS:
    VALIDATORS.remove('checkNewsImageMaxSize')
if 'isMaxSize' in VALIDATORS:
    VALIDATORS.remove('isMaxSize')
if 'isTAL' in VALIDATORS:
    VALIDATORS.remove('isTAL')
if 'checkFileMaxSize' in VALIDATORS:
    VALIDATORS.remove('checkFileMaxSize')
if 'isNonEmptyFile' in VALIDATORS:
    VALIDATORS.remove('isNonEmptyFile')
if 'isEmptyNoError' in VALIDATORS:
    VALIDATORS.remove('isEmptyNoError')
if 'isTidyHtml' in VALIDATORS:
    VALIDATORS.remove('isTidyHtml')
if 'isUnixLikeName' in VALIDATORS:
    VALIDATORS.remove('isUnixLikeName')
if 'isTidyHtmlWithCleanup' in VALIDATORS:
    VALIDATORS.remove('isTidyHtmlWithCleanup')
if 'inNumericRange' in VALIDATORS:
    VALIDATORS.remove('inNumericRange')
if 'isPrintable' in VALIDATORS:
    VALIDATORS.remove('isPrintable')

TEXT_VALIDATORS = VALIDATORS
