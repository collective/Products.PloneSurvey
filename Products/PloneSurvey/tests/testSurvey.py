#
# Test PloneSurvey Survey
#

import os, sys
from DateTime import DateTime
#from AccessControl import Unauthorized
from Testing.makerequest import makerequest
from Products.CMFFormController.ControllerState import ControllerState
from Products.CMFCore.utils import getToolByName

from base import PloneSurveyTestCase

class TestSurvey(PloneSurveyTestCase):
    """Ensure survey validation"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.addMember('survey_user', 'Survey User', 'survey@here.com', 'Member', DateTime())
        self.addMember('no_name_user', '', 'survey@here.com', 'Member', DateTime())

    def testCanGetFullName(self):
        s1 = getattr(self, 's1')
        userid = s1.getRespondentFullName('survey_user')
        assert userid == "Survey User", "Not user fullname: %s" % userid

    def testNoFullName(self):
        s1 = getattr(self, 's1')
        userid = s1.getRespondentFullName('no_name_user')
        assert userid == "no_name_user", "Not user id: %s" % userid

    def testAnonFullName(self):
        s1 = getattr(self, 's1')
        userid = s1.getRespondentFullName('Anonymous')
        assert userid is None, "Something returned for anonymous"

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSurvey))
    return suite
