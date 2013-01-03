from Products.CMFCore.permissions import setDefaultRoles

from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.permissions import ManageProperties
from Products.CMFCore.permissions import ManagePortal

addSurvey = 'PloneSurvey: Add Survey'
# N.B. Use of this permission is hard-coded in survey_view skin template!
ResetOwnResponses = 'PloneSurvey: Reset Own Responses'
ViewSurveyResults = 'PloneSurvey: View Survey Results'

setDefaultRoles(ViewSurveyResults,('Manager', 'Owner'))
