from Products.CMFCore.permissions import setDefaultRoles

from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.permissions import ManageProperties
from Products.CMFCore.permissions import ManagePortal

from config import PROJECTNAME

# N.B. Use of this permission is hard-coded in survey_view skin template!
addSurvey = '%s: Add Survey' % PROJECTNAME
ResetOwnResponses = '%s: Reset Own Responses' % PROJECTNAME
ViewSurveyResults = '%s: View Survey Results' % PROJECTNAME

setDefaultRoles(ViewSurveyResults,('Manager', 'Owner'))
