#
# Test PloneSurvey add answer
#

import os, sys
from DateTime import DateTime
from AccessControl import Unauthorized

from base import PloneSurveyTestCase

class TestAnonymousId(PloneSurveyTestCase):
    """Ensure survey select question can be answered"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)

    def testAnonymousIdGeneration(self):
        s1 = getattr(self, 's1')
        now = DateTime()
        self.logout()
        userid = s1.getSurveyId()
        expected_userid = 'Anonymous' + '@' + str(now)
        assert userid[:-9] == expected_userid[:-9], "Anonymous id generation not working - %s" % userid

class TestAddAnswer(PloneSurveyTestCase):
    """Ensure survey question can be answered"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')
        stq1.setRequired(True)

    def testAddAnswer(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Text answer')
                assert question.getAnswerFor(userid) == 'Text answer', "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)

    def testAnonymousAddAnswer(self):
        s1 = getattr(self, 's1')
        self.logout()
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Anonymous Text answer')
                # need to login as original user, as anonymous cannot getAnswer
                self.login("test_user_1_")
                users = s1.getRespondents()
                assert len(users) == 1, 'More than one user responded'
                assert question.getAnswerFor(users[0]) == 'Anonymous Text answer', "Answer not saved correctly"

    def testAnonymousCantAddAnswer(self):
        s1 = getattr(self, 's1')
        stq1 = getattr(self.s1, 'stq1')
        s1.setAllowAnonymous(False)
        self.logout()
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                self.assertRaises(Unauthorized,
                    question.addAnswer,
                    'Anonymous Text answer')

class TestAddSelectAnswer(PloneSurveyTestCase):
    """Ensure survey select question can be answered"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        ssq1 = getattr(self.s1, 'ssq1')

    def testAddAnswer(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Select Question':
                question.addAnswer('Yes')
                assert question.getAnswerFor(userid) == 'Yes', "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAnonymousId))
    suite.addTest(makeSuite(TestAddAnswer))
    suite.addTest(makeSuite(TestAddSelectAnswer))
    return suite
