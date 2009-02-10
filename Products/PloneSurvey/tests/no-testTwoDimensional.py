#
# Test PloneSurvey Two Dimensional
#

import os, sys
from AccessControl import Unauthorized

from Testing.makerequest import makerequest
from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from base import PloneSurveyTestCase

class testTwoDimensional(PloneSurveyTestCase):
    """Test the two dimensional question types"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.invokeFactory('Survey Two Dimensional', 'std1')
        std1 = getattr(self.s1, 'std1')
        std1.at_post_create_script()

    def testCheckQuestionsAdded(self):
        s1 = getattr(self, 's1')
        std1 = getattr(s1, 'std1')
        self.failUnless('std1-dimension-one' in std1.objectIds())
        self.failUnless('std1-dimension-two' in std1.objectIds())

    def testQuestionTitles(self):
        s1 = getattr(self, 's1')
        std1 = getattr(s1, 'std1')
        std1dim1 = getattr(std1, 'std1-dimension-one')
        assert std1dim1.Title() == 'std1 Dimension One', "Title not correct"

    def testViewMethod(self):
        s1 = getattr(self, 's1')
        std1 = getattr(s1, 'std1')
        std1dim1 = getattr(std1, 'std1-dimension-one')
        view_method = std1dim1()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testTwoDimensional))
    return suite
