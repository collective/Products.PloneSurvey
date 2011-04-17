#
# Test PloneSurvey permissions
#

from AccessControl import getSecurityManager
from DateTime import DateTime
from ZPublisher.BaseRequest import BaseRequest as Request

from Products.PloneSurvey import permissions

from base import PloneSurveyTestCase

class TestPermissions(PloneSurveyTestCase):
    """Test permissions work correctly"""

    def afterSetUp(self):
        self.createAnonSurvey()
        # need to log in as another user as the test user has owner role here
        self.addMember('survey_user', 'Survey User', 'survey@here.com', ['Contributor',], DateTime())
        self.logout()
        self.login('survey_user')

    def testResultsPermission(self):
        s1 = getattr(self.folder, 's1')
        assert getSecurityManager().checkPermission(permissions.ViewSurveyResults, s1)

    def testResultsView(self):
        s1 = getattr(self.folder, 's1')
        result = s1.survey_view_results(REQUEST=Request())
        self.assertEqual(result.find('Please log in') >= 0, False)
