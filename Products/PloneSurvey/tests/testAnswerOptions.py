#
# Test PloneSurvey answer options
#

import os, sys
from AccessControl import Unauthorized

from Products.Archetypes.utils import DisplayList

from base import PloneSurveyTestCase

class TestAnswerOptions(PloneSurveyTestCase):
    """Ensure survey question can be answered"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testSelectQuestionOptions(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        assert ssq1.getQuestionOptions() == ssq1.getAnswerOptions(), "Options not returned correctly"
        ssq1.setLikertOptions('1')
        assert isinstance(ssq1.getQuestionOptions(), DisplayList), "Likert options not returned correctly"
        options = ssq1.getQuestionOptions()
        assert options[0] == 5, "Key of likert option wrong"
        assert options.getValue(5) == 'Very Good', "Value of likert option wrong"
        assert len(ssq1.getQuestionOptions()) == 5, "Wrong number of likert options returned: %s" % ssq1.getQuestionOptions()
        ssq1.setNullValue('Not applicable')
        assert len(ssq1.getQuestionOptions()) == 6, "Wrong number of likert options returned: %s" % ssq1.getQuestionOptions()
        assert ssq1.getQuestionOptions().getValue(0) == 'Not applicable', "Null option not first"

    def testSelectQuestionOptionsOrderVocabOption1(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setLikertOptions('1')
        ssq1.setReverseLikert(True)
        options = ssq1.getQuestionOptions()
        assert options[0] == 1, "Key of likert option wrong"

    def testSelectQuestionOptionsOrderOption2(self):
        s1 = getattr(self, 's1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setLikertOptions('2')
        ssq1.setReverseLikert(True)
        options = ssq1.getQuestionOptions()
        assert options[0] == 1, "Key of likert option wrong"

    def testMatrixQuestionOptions(self):
        s1 = getattr(self, 's1')
        sm1 = getattr(s1, 'sm1')
        smq1 = getattr(sm1, 'smq1')
        assert smq1.getQuestionOptions() == sm1.getAnswerOptions(), "Options not returned correctly"
        sm1.setLikertOptions('1')
        assert isinstance(smq1.getQuestionOptions(), DisplayList), "Likert options not returned correctly"
        options = smq1.getQuestionOptions()
        assert options[0] == 5, "Key of likert option wrong"
        assert options.getValue(5) == 'Very Good', "Value of likert option wrong"
        assert len(smq1.getQuestionOptions()) == 5, "Wrong number of likert options returned"
        smq1.setNullValue('Not applicable')
        assert len(smq1.getQuestionOptions()) == 6, "Wrong number of likert options returned"
        assert smq1.getQuestionOptions().getValue(0) == 'Not applicable', "Null option not first"

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAnswerOptions))
    return suite
