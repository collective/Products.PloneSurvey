#
# Test PloneSurvey Survey
#

import os, sys
from DateTime import DateTime
from AccessControl import Unauthorized

from base import PloneSurveyTestCase

class TestRespondentDetails(PloneSurveyTestCase):
    """Ensure respondent is added to survey object"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')

    def testRespondentsPropertyd(self):
        """check respondent attribute created"""
        s1 = getattr(self, 's1')
        assert hasattr(s1, 'respondents')

    def testRespondentAdded(self):
        s1 = getattr(self, 's1')
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 0
        userid = s1.getSurveyId()
        assert userid == "test_user_1_"
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 1
        respondent = respondents['test_user_1_']
        assert respondent.has_key('start')
        assert respondent.has_key('end')
        assert respondent.has_key('ip_address')

    def testRespondentReset(self):
        s1 = getattr(self, 's1')
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 0
        userid = s1.getSurveyId()
        assert userid == "test_user_1_"
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 1
        s1.reset()
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 0

    def testRespondentResetForUser(self):
        s1 = getattr(self, 's1')
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 0
        userid = s1.getSurveyId()
        assert userid == "test_user_1_"
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 1
        s1.resetForUser('test_user_1_')
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 0

    def testRespondentResetForAuthenticatedUser(self):
        s1 = getattr(self, 's1')
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 0
        userid = s1.getSurveyId()
        assert userid == "test_user_1_"
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 1
        s1.resetForAuthenticatedUser()
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 0

    def testRespondentsList(self):
        s1 = getattr(self, 's1')
        respondents = s1.getRespondentsDetails()
        assert len(respondents) == 0
        userid = s1.getSurveyId()
        assert userid == "test_user_1_"
        respondents = s1.getRespondentsList()
        assert len(respondents) == 1
        assert "test_user_1_" in respondents

    def testRespondentDetails(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_"
        respondent = s1.getRespondentDetails("test_user_1_")
        assert respondent.has_key('start')
        assert respondent.has_key('end')
        assert respondent.has_key('ip_address')

    def testEndTimeAdded(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_"
        s1.setCompletedForUser()
        respondent = s1.getRespondentDetails("test_user_1_")
        assert respondent['end'] != ''

class TestResetOwnResponse(PloneSurveyTestCase):
    """Ensure user can reset their own response"""

    def afterSetUp(self):
        self.createAnonSurvey()
        self.folder.s1.invokeFactory('Survey Text Question', 'stq1')

    def testResetOwnResponse(self):
        """Ensure user can reset their own response"""
        s1 = getattr(self.folder, 's1')
        s1.setCompletedForUser()
        assert len(s1.getRespondentsList()) == 1
        s1.resetForAuthenticatedUser()
        assert len(s1.getRespondentsList()) == 0

    def testResetOwnResponseUser(self):
        """Ensure user can reset their own response"""
        s1 = getattr(self.folder, 's1')
        s1.setCompletedForUser()
        assert len(s1.getRespondentsList()) == 1
        s1.resetForUser('test_user_1_')
        assert len(s1.getRespondentsList()) == 0

class TestCanNotResetResponse(PloneSurveyTestCase):
    """Ensure user can not reset another response"""

    def afterSetUp(self):
        self.addMember('survey_user', 'Survey User', 'survey@here.com', 'Member', DateTime())
        self.createAnonSurvey()
        self.folder.s1.invokeFactory('Survey Text Question', 'stq1')
        self.logout()

    def testResetOwnResponse(self):
        """Ensure user can reset their own response"""
        self.login('survey_user')
        s1 = getattr(self.folder, 's1')
        s1.setCompletedForUser()
        self.setRoles(('Authenticated',))
        assert len(s1.getRespondentsList()) == 1
        s1.resetForAuthenticatedUser()
        assert len(s1.getRespondentsList()) == 0

    def testCantResetFromResetMethod(self):
        """Ensure user can't reset response from underlying method"""
        self.login('survey_user')
        s1 = getattr(self.folder, 's1')
        s1.setCompletedForUser()
        assert len(s1.getRespondentsList()) == 1
        self.logout()
        self.assertRaises(Unauthorized,
                          s1.resetForUser,
                          'survey_user')
        assert len(s1.getRespondentsList()) == 1

    def testAnonymousCantResetFromResetMethod(self):
        """Ensure anonymous user can't reset response"""
        self.logout()
        s1 = getattr(self.folder, 's1')
        s1.setCompletedForUser()
        assert len(s1.getRespondentsList()) == 1
        self.assertRaises(Unauthorized,
                          s1.resetForUser,
                          'survey_user')
        assert len(s1.getRespondentsList()) == 1

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

class TestAddAnswer(PloneSurveyTestCase):
    """Ensure survey question can be answered"""

    def afterSetUp(self):
        self.createAnonSurvey()
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

class TestBarchart(PloneSurveyTestCase):
    """Ensure survey barchart works correctly"""

    def afterSetUp(self):
        """Build a survey with a range of questions"""
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')
        self.s1.invokeFactory('Sub Survey', 'sub1')
        self.s1.sub1.invokeFactory('Survey Select Question', 'ssq2')
        self.s1.sub1.invokeFactory('Survey Text Question', 'stq2')
        self.s1.sub1.invokeFactory('Survey Matrix', 'sm2')
        self.s1.sub1.sm2.invokeFactory('Survey Matrix Question', 'smq2')

    def testBarchartColours(self):
        s1 = getattr(self, 's1')
        colours = s1.getSurveyColors(0)
        assert colours is not None

class TestReturnsQuestions(PloneSurveyTestCase):
    """Ensure survey returns correct questions"""

    def afterSetUp(self):
        """Build a survey with a range of questions"""
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        self.s1.invokeFactory('Survey Matrix', 'sm1')
        self.s1.sm1.invokeFactory('Survey Matrix Question', 'smq1')
        self.s1.invokeFactory('Sub Survey', 'sub1')
        self.s1.sub1.invokeFactory('Survey Select Question', 'ssq2')
        self.s1.sub1.invokeFactory('Survey Text Question', 'stq2')
        self.s1.sub1.invokeFactory('Survey Matrix', 'sm2')
        self.s1.sub1.sm2.invokeFactory('Survey Matrix Question', 'smq2')

    def testAllQuestions(self):
        s1 = getattr(self, 's1')
        self.assertEqual(len(s1.getAllQuestions()), 6)
        self.assertEqual(len(s1.getQuestions()), 3)
        self.assertEqual(len(s1.getAllQuestionsInOrder()), 8)
        self.assertEqual(len(s1.getAllQuestionsInOrder(include_sub_survey=True)), 9)
        self.assertEqual(len(s1.getAllSelectQuestionsInOrder()), 4)

    def testAllSelectQuestionsOrder(self):
        s1 = getattr(self, 's1')
        questions = s1.getAllSelectQuestionsInOrder()
        self.assertEqual(questions[0].getId(), 'ssq1')
        self.assertEqual(questions[1].getId(), 'smq1')
        self.assertEqual(questions[2].getId(), 'ssq2')
        self.assertEqual(questions[3].getId(), 'smq2')

    def testMoveObjects(self):
        s1 = getattr(self, 's1')
        s1.moveObjectsToTop(['sm1',])
        self.portal.portal_catalog.clearFindAndRebuild()
        questions = s1.getAllSelectQuestionsInOrder()
        self.assertEqual(questions[0].getId(), 'smq1')
        self.assertEqual(questions[1].getId(), 'ssq1')
        self.assertEqual(questions[2].getId(), 'ssq2')
        self.assertEqual(questions[3].getId(), 'smq2')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRespondentDetails))
    suite.addTest(makeSuite(TestResetOwnResponse))
    # XXX security context isn't available from unit test
    #suite.addTest(makeSuite(TestCanNotResetResponse))
    suite.addTest(makeSuite(TestSurvey))
    suite.addTest(makeSuite(TestAddAnswer))
    suite.addTest(makeSuite(TestAddSelectAnswer))
    suite.addTest(makeSuite(TestBarchart))
    suite.addTest(makeSuite(TestReturnsQuestions))
    return suite
