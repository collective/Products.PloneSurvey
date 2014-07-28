from Products.CMFCore.permissions import setDefaultRoles

addSurvey = 'PloneSurvey: Add Survey'
# N.B. Use of this permission is hard-coded in survey_view skin template!
ResetOwnResponses = 'PloneSurvey: Reset Own Responses'
ViewSurveyResults = 'PloneSurvey: View Survey Results'

setDefaultRoles(ViewSurveyResults, ('Manager', 'Owner'))
