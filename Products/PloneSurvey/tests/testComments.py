#
# Test PloneSurvey Comments
#

import os, sys
#from AccessControl import Unauthorized
from Testing.makerequest import makerequest
from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from base import PloneSurveyTestCase

class TestSelectComment(PloneSurveyTestCase):
    """Ensure survey validation"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        self.s1.ssq1.setCommentType('text')

    def testAnswerWithComment(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        userid = s1.getSurveyId()
        ssq1.addAnswer('Yes', 'Comment')
        assert ssq1.getAnswerFor(userid) == 'Yes', "Answer not saved correctly"
        assert ssq1.getCommentsFor(userid) == 'Comment', "Comment not saved correctly"

    def testNoAnswerWithComment(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        userid = s1.getSurveyId()
        ssq1.addAnswer('', 'Comment')
        assert ssq1.getAnswerFor(userid) == '', "Answer not saved correctly"
        assert ssq1.getCommentsFor(userid) == 'Comment', "Comment not saved correctly"

    def testValidatesAnswerWithComment(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        userid = s1.getSurveyId()
        app = makerequest(self.app)
        app.REQUEST.form['ssq1'] = 'Yes'
        app.REQUEST.form['ssq1_comments'] = 'Comment'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert ssq1.getAnswerFor(userid) == 'Yes', "Answer not saved correctly"
        assert ssq1.getCommentsFor(userid) == 'Comment', "Comment not saved correctly"

    def testValidatesNoAnswerWithComment(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        userid = s1.getSurveyId()
        app = makerequest(self.app)
        app.REQUEST.form['ssq1'] = ''
        app.REQUEST.form['ssq1_comments'] = 'Comment'
        dummy_controller_state = ControllerState(
                                    id='survey_view',
                                    context=s1,
                                    button='submit',
                                    status='success',
                                    errors={},
                                    next_action=None,)
        controller = self.portal.portal_form_controller
        controller_state = controller.validate(dummy_controller_state, app.REQUEST, ['validate_survey',])
        assert ssq1.getAnswerFor(userid) == '', "Answer not saved correctly: %s" %ssq1.getAnswerFor(userid)
        assert ssq1.getCommentsFor(userid) == 'Comment', "Comment not saved correctly"

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSelectComment))
    return suite
