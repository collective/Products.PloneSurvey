PROJECTNAME = "PloneSurvey"

from Products.Archetypes.utils import DisplayList
from Products.Archetypes.utils import IntDisplayList
from Products.validation import validation

import permissions

# Import "PloneSurveyMessageFactory as _" to create messages in plonesurvey domain
from zope.i18nmessageid import MessageFactory
PloneSurveyMessageFactory = _ = MessageFactory('plonesurvey')

ADD_CONTENT_PERMISSION = permissions.AddPortalContent
SKINS_DIR = 'skins'

GLOBALS = globals()

try:
    from reportlab.lib import colors
except ImportError:
    HAS_REPORTLAB = False
else:
    HAS_REPORTLAB = True

DEFAULT_SURVEY_INVITE = u'''
<p>Dear **Name**,</p>
<p>Please complete the **Survey**</p>
<p>Thank you</p>'''

SURVEY_STATUS = DisplayList((
    ('open', 'Open', 'label_survey_open'),
    ('closed', 'Closed', 'label_survey_closed'),
    ))

NOTIFICATION_METHOD = DisplayList((
    ('', _(u'label_no_emails', default=u'No emails')),
    ('each_submission', _(u'label_all_emails', default=u'Email on each submission')),
    ))

TEXT_INPUT_TYPE = DisplayList((
    ('text', 'Text Field', 'label_text_field'),
    ('area', 'Text Area', 'label_text_area'),
    ))

SELECT_INPUT_TYPE = DisplayList((
    ('radio', 'Radio Buttons', 'label_radio_buttons'),
    ('selectionBox', 'Selection Box', 'label_selection_box'),
    ('multipleSelect', 'Multiple Selection Box', 'label_multiple_selection_box'),
    ('checkbox', 'Check Boxes', 'label_check_boxes'),
    ))

INPUT_TYPE = DisplayList((
    ('radio', 'Radio Buttons', 'label_radio_buttons'),
    ('selectionBox', 'Selection Box', 'label_selection_box'),
    ('text', 'Text Field', 'label_text_field'),
    ('area', 'Text Area', 'label_text_area'),
    ('multipleSelect', 'Multiple Selection Box', 'label_multiple_selection_box'),
    ('checkbox', 'Check Boxes', 'label_check_boxes'),
    ))

TEXT_LOCATION = IntDisplayList((
    (0, 'Does not appear', 'XXX'),
    (1, 'Appears above question', 'XXX'),
    (2, 'Appears between question and answer', 'XXX'),
    (3, 'Appears after answer', 'XXX'),
    ))

COMMENT_TYPE = DisplayList((
    ('', 'None', 'label_no_comment_field'),
    ('text', 'Text Field', 'label_text_field'),
    ('area', 'Text Area', 'label_text_area'),
    ))
    
TWO_D_INPUT_TYPE = DisplayList((
    ('radio', 'Radio Buttons', 'label_radio_buttons'),
    ('selectionBox', 'Selection Box', 'label_selection_box'),
    ))

LIKERT_OPTIONS = IntDisplayList((
    (0, 'Use the options below', 'XXX'),
    (1, '("Very Good", "Good", "OK Only", "Poor", "Very Poor")', 'XXX'),
    (2, '("Very Useful", "Useful", "Quite Useful", "A little Useful", "Not Useful")', 'XXX'),
    (3, '("Agree Strongly", "Agree", "Neutral", "Disagree", "Disagree Strongly")', 'XXX'),
    ))

LIKERT_OPTIONS_MAP = {
    1 : IntDisplayList((
        (5, 'Very Good', 'Very Good'),
        (4, 'Good', 'Good'),
        (3, 'OK Only', 'OK Only'),
        (2, 'Poor', 'Poor'),
        (1, 'Very Poor', 'Very Poor'),
        )),
    2 : IntDisplayList((
        (5, 'Very Useful', 'Very Useful'),
        (4, 'Useful', 'Useful'),
        (3, 'Quite Useful', 'Quite Useful'),
        (2, 'A little Useful', 'A little Useful'),
        (1, 'Not Useful', 'Not Useful'),
        )),
    3 : IntDisplayList((
        (5, 'Agree Strongly', 'Agree Strongly'),
        (4, 'Agree', 'Agree'),
        (3, 'Neutral', 'Neutral'),
        (2, 'Disagree', 'Disagree'),
        (1, 'Disagree Strongly', 'Disagree Strongly'),
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
