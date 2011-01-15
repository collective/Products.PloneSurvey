from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

from Products.PloneSurvey.config import PROJECTNAME, GLOBALS, HAS_REPORTLAB

def install(self):
    out = StringIO()

    portal_setup = getToolByName(self, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Products.PloneSurvey:default')
    # Create External methods
    if HAS_REPORTLAB:
        if not hasattr(self, 'get_2d_chart'):
            em = self.manage_addProduct['ExternalMethod']
            em.manage_addExternalMethod('get_2d_chart', 'get_2d_chart', 'PloneSurvey.get_2d_chart', 'run')   
        if not hasattr(self, 'results_questions'):
            em = self.manage_addProduct['ExternalMethod']
            em.manage_addExternalMethod('results_questions', 'results_questions', 'PloneSurvey.results_questions', 'run')   
        if not hasattr(self, 'results_dimensions'):
            em = self.manage_addProduct['ExternalMethod']
            em.manage_addExternalMethod('results_dimensions', 'results_dimensions', 'PloneSurvey.results_dimensions', 'run')   

    #self.manage_permission(perms.VIEW_SURVEY_RESULTS_PERMISSION,
    #                             ('Manager', 'Owner'),
    #                             acquire=1)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()
