import unittest

from AccessControl import Unauthorized

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, setRoles
from plone.app.testing import login, logout
from Products.CMFCore.utils import getToolByName

from base import INTEGRATION_TESTING, INTEGRATION_ANON_SURVEY_TESTING


class TestRespondentDetails(unittest.TestCase):
    """Ensure respondent is added to survey object"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')

    def testRespondentsPropertyCreated(self):
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
        assert 'start' in respondent
        assert 'end' in respondent
        assert 'ip_address' in respondent

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
        assert 'start' in respondent
        assert 'end' in respondent
        assert 'ip_address' in respondent

    def testEndTimeAdded(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_"
        s1.setCompletedForUser()
        respondent = s1.getRespondentDetails("test_user_1_")
        assert respondent['end'] != ''


class TestResetOwnResponse(unittest.TestCase):
    """Ensure user can reset their own response"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.s1.invokeFactory('Survey Text Question', 'stq1')

    def testResetOwnResponse(self):
        """Ensure user can reset their own response"""
        s1 = getattr(self.portal, 's1')
        s1.setCompletedForUser()
        assert len(s1.getRespondentsList()) == 1
        s1.resetForAuthenticatedUser()
        assert len(s1.getRespondentsList()) == 0

    def testResetOwnResponseUser(self):
        """Ensure user can reset their own response"""
        s1 = getattr(self.portal, 's1')
        s1.setCompletedForUser()
        assert len(s1.getRespondentsList()) == 1
        s1.resetForUser('test_user_1_')
        assert len(s1.getRespondentsList()) == 0


class TestCanNotResetResponse(unittest.TestCase):
    """Ensure user can not reset another response"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_membership = getToolByName(self.portal,
                                               'portal_membership')
        self.portal_membership.addMember(
            'survey_user',
            'secret',
            ['Member', ],
            [],
            {'fullname': 'Survey User', 'email': 'survey@here.com', }
        )
        self.portal.s1.invokeFactory('Survey Text Question', 'stq1')
        logout()

    def testResetOwnResponse(self):
        """Ensure user can reset their own response"""
        login(self.portal, 'survey_user')
        s1 = getattr(self.portal, 's1')
        s1.setCompletedForUser()
        setRoles(self.portal, TEST_USER_ID, ['Authenticated'])
        assert len(s1.getRespondentsList()) == 1
        s1.resetForAuthenticatedUser()
        assert len(s1.getRespondentsList()) == 0

# =============================================================================
#    def testCantResetFromResetMethod(self):
#        """Ensure user can't reset response from underlying method"""
#        login(self.portal, 'survey_user')
#        s1 = getattr(self.portal, 's1')
#        s1.setCompletedForUser()
#        assert len(s1.getRespondentsList()) == 1
#        logout()
#        self.assertRaises(Unauthorized,
#                          s1.resetForUser,
#                          'survey_user')
#        assert len(s1.getRespondentsList()) == 1
#
#    def testAnonymousCantResetFromResetMethod(self):
#        """Ensure anonymous user can't reset response"""
#        logout()
#        s1 = getattr(self.portal, 's1')
#        s1.setCompletedForUser()
#        assert len(s1.getRespondentsList()) == 1
#        self.assertRaises(Unauthorized,
#                          s1.resetForUser,
#                          'survey_user')
#        assert len(s1.getRespondentsList()) == 1
# =============================================================================


class TestSurvey(unittest.TestCase):
    """Ensure survey validation"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.portal_membership = getToolByName(self.portal,
                                               'portal_membership')
        self.portal_membership.addMember(
            'survey_user',
            'secret',
            ['Member', ],
            [],
            {'fullname': 'Survey User', 'email': 'survey@here.com', }
        )
        self.portal_membership.addMember(
            'no_name_user',
            'secret',
            ['Member', ],
            [],
            {'fullname': '', 'email': 'survey@here.com', }
        )

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


class TestAddAnswer(unittest.TestCase):
    """Ensure survey question can be answered"""
    layer = INTEGRATION_ANON_SURVEY_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.portal.s1, 'stq1')
        stq1.setRequired(True)

    def testAddAnswer(self):
        s1 = getattr(self.portal, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Text answer')
                assert question.getAnswerFor(userid) == 'Text answer', \
                    "Answer not saved correctly"
        answers = s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)

    def testAnonymousAddAnswer(self):
        s1 = getattr(self.portal, 's1')
        logout()
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                question.addAnswer('Anonymous Text answer')
                # need to login as original user, as anonymous cannot getAnswer
                login(self.portal, TEST_USER_NAME)
                users = s1.getRespondentsList()
                assert len(users) == 1, 'More than one user responded'
                assert question.getAnswerFor(users[0]) == \
                    'Anonymous Text answer', "Answer not saved correctly"

    def testAnonymousCantAddAnswer(self):
        s1 = getattr(self.portal, 's1')
        s1.setAllowAnonymous(False)
        logout()
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Text Question':
                self.assertRaises(
                    Unauthorized,
                    question.addAnswer,
                    'Anonymous Text answer'
                )


class TestAddSelectAnswer(unittest.TestCase):
    """Ensure survey select question can be answered"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
        self.s1.setAllowAnonymous(True)
        self.s1.invokeFactory('Survey Select Question', 'ssq1')

    def testAddAnswer(self):
        s1 = getattr(self, 's1')
        userid = s1.getSurveyId()
        assert userid == "test_user_1_", "Not default test user"
        questions = s1.getQuestions()
        for question in questions:
            if question.portal_type == 'Survey Select Question':
                question.addAnswer('Yes')
                assert question.getAnswerFor(userid) == 'Yes', \
                    "Answer not saved correctly"
        answers = self.s1.getAnswersByUser(userid)
        self.assertEqual(len(answers), 1)


class TestBarchart(unittest.TestCase):
    """Ensure survey barchart works correctly"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        """Build a survey with a range of questions"""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
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


class TestReturnsQuestions(unittest.TestCase):
    """Ensure survey returns correct questions"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        """Build a survey with a range of questions"""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')
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
        self.assertEqual(len(s1.getAllQuestionsInOrder(
            include_sub_survey=True)), 9)
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
        s1.moveObjectsToTop(['sm1', ])
        self.portal.portal_catalog.clearFindAndRebuild()
        questions = s1.getAllSelectQuestionsInOrder()
        self.assertEqual(questions[0].getId(), 'smq1')
        self.assertEqual(questions[1].getId(), 'ssq1')
        self.assertEqual(questions[2].getId(), 'ssq2')
        self.assertEqual(questions[3].getId(), 'smq2')
