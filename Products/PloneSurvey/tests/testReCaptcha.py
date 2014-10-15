import unittest2 as unittest

from ZPublisher.BaseRequest import BaseRequest as Request

from Products.CMFFormController.ControllerState import ControllerState
from plone.app.testing import TEST_USER_ID, setRoles

from base import INTEGRATION_RECAPTCHA_TESTING

from collective.recaptcha.settings import getRecaptchaSettings


class testReCaptcha(unittest.TestCase):
    """Ensure captcha works correctly"""
    layer = INTEGRATION_RECAPTCHA_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        self.s1.setShowCaptcha(True)
        recapcha_settings = getRecaptchaSettings()
        recapcha_settings.public_key = 'foo'
        recapcha_settings.private_key = 'bar'
        self.layer['request'].set('ACTUAL_URL', self.s1.absolute_url())

    def testIncludeReCaptcha(self):
        """Test if captcha is included in the page"""
        result = self.s1.survey_view(REQUEST=Request())
        assert "<input type='hidden' name='recaptcha_response_field' value='manual_challenge' />" in result

    def testValidationReCaptcha(self):
        """Test if captcha works"""
        self.layer['request'].form['stq1'] = 'test'
        dummy_controller_state = ControllerState(
            id='survey_view',
            context=self.s1,
            button='submit',
            status='success',
            errors={},
            next_action=None,
        )
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(
            dummy_controller_state,
            self.layer['request'],
            ['validate_survey', ]
        )
        assert controller_state.getErrors() != {}, \
            "Validation error raised: %s" % controller_state.getErrors()
