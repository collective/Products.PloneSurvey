#
# Test PloneSurvey Branching
#

import os, sys

from base import PloneSurveyTestCase

class TestBranching(PloneSurveyTestCase):
    """Test Survey Branching"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        s1 = getattr(self.folder, 's1')
        s1.invokeFactory('Survey Select Question', 'ssq1')
        s1.invokeFactory('Sub Survey', 'ss1')
        s1.invokeFactory('Sub Survey', 'ss2')

    def testEditSubSurveyBranch(self):
        s1 = getattr(self.folder, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ss1 = getattr(s1, 'ss1')
        ss2 = getattr(s1, 'ss2')
        ss1.setRequiredQuestion('ssq1')
        ss1.setRequiredAnswer(1)
        self.assertEqual(ss1.getRequiredQuestion(), 'ssq1')
        self.assertEqual(ss1.getRequiredAnswer(), 1)

    def testSingleBranchChoice(self):
        s1 = getattr(self.folder, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ss1 = getattr(s1, 'ss1')
        ss2 = getattr(s1, 'ss2')
        ssq1.addAnswer('Yes')
        ss1.setRequiredQuestion('ssq1')
        ss1.setRequiredAnswer(1)
        ss2.setRequiredQuestion('ssq1')
        ss2.setRequiredAnswer(0)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestBranching))
    return suite
