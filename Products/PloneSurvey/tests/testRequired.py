#
# Test PloneSurvey required fields
#

import os, sys

from Products.CMFCore.utils import getToolByName

from base import PloneSurveyTestCase

class TestRequired(PloneSurveyTestCase):
    """Ensure required field works correctly"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')

    def testSurveyMatrix(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        assert sm1.getRequired() == 1, "Matrix default should be required"
        sm1.setNullValue('Not applicable')
        assert sm1.getRequired() == 0, "Should be required when nullValue exists"

    def testSurveyMatrixQuestion(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        assert smq1.getRequired() == 1, "Matrix Question default should be required"
        sm1.setNullValue('Not applicable')
        assert smq1.getRequired() == 0, "Should be required when nullValue exists"

    def testSurveySelectQuestion(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        assert ssq1.getRequired() == 1, "Select Question default should be required"
        ssq1.setNullValue('Not applicable')
        assert ssq1.getRequired() == 0, "Should be required when nullValue exists"

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRequired))
    return suite
