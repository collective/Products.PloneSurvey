#
# Test PloneSurvey initialisation and set-up
#

import os, sys

from Products.PloneSurvey import permissions
from base import PloneSurveyTestCase

class TestInstallation(PloneSurveyTestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.css        = self.portal.portal_css
        self.kupu       = self.portal.kupu_library_tool
        self.skins      = self.portal.portal_skins
        self.types      = self.portal.portal_types
        self.factory    = self.portal.portal_factory
        self.workflow   = self.portal.portal_workflow
        self.properties = self.portal.portal_properties

        self.metaTypes = ('Survey',
                          'Sub Survey',
                          'Survey Matrix',
                          'Survey Matrix Question',
                          'Survey Select Question',
                          #'Survey Two Dimensional',
                          #'Survey 2-Dimensional Question',
                          'Survey Text Question')

    def testCssInstalled(self):
        self.failUnless('survey_results.css' in self.css.getResourceIds())

    def testSkinLayersInstalled(self):
        self.failUnless('plone_survey' in self.skins.objectIds())

    def testPortalFactorySetup(self):
        self.failUnless('Survey' in self.factory.getFactoryTypes())

    def testTypesInstalled(self):
        for t in self.metaTypes:
            self.failUnless(t in self.types.objectIds())

    def testMetaTypesNotToList(self):
        for t in self.metaTypes:
            if t not in ['Survey', 'Sub Survey']:
                self.failUnless(t in self.properties.navtree_properties.metaTypesNotToList)

    def testPermissions(self):
        """
        Test permissions are configured correctly
        """
        roles = self.portal.rolesOfPermission(permissions.ResetOwnResponses)
        for role in roles:
            if role['name'] == 'Member':
                self.failUnless(role['selected'])
        roles = self.portal.rolesOfPermission(permissions.ViewSurveyResults)
        for role in roles:
            if role['name'] == 'Owner':
                self.failUnless(role['selected'])

class TestContentCreation(PloneSurveyTestCase):
    """Ensure content types can be created and edited"""

    def afterSetUp(self):
        self.folder.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.folder, 's1')

    def testCreateSurvey(self):
        self.failUnless('s1' in self.folder.objectIds())

    def testEditSurvey(self):
        self.s1.setTitle('A title')
        self.s1.setDescription('A description')

        self.assertEqual(self.s1.Title(), 'A title')
        self.assertEqual(self.s1.Description(), 'A description')

    def testSurveyAllowedTypes(self):
        s1 = getattr(self, 's1')
        s1.invokeFactory('Survey Matrix', 'sm1')
        self.failUnless('sm1' in s1.objectIds())
        s1.invokeFactory('Survey Select Question', 'ssq1')
        self.failUnless('ssq1' in s1.objectIds())
        s1.invokeFactory('Survey Text Question', 'stq1')
        self.failUnless('stq1' in s1.objectIds())
        #s1.invokeFactory('Survey Two Dimensional', 'std1')
        #self.failUnless('std1' in s1.objectIds())

    def testCreateSubSurvey(self):
        self.s1.invokeFactory('Sub Survey', 'ss1')
        self.failUnless('ss1' in self.s1.objectIds())
        
    def testEditSubSurvey(self):
        self.s1.invokeFactory('Sub Survey', 'ss1')
        ss1 = getattr(self.s1, 'ss1')

        ss1.setTitle('Sub Survey title')
        ss1.setDescription('Sub Survey description')

        self.assertEqual(ss1.Title(), 'Sub Survey title')
        self.assertEqual(ss1.Description(), 'Sub Survey description')

    def testSubSurveyAllowedTypes(self):
        self.s1.invokeFactory('Sub Survey', 'ss1')
        ss1 = getattr(self.s1, 'ss1')
        ss1.invokeFactory('Survey Matrix', 'sm1')
        self.failUnless('sm1' in ss1.objectIds())
        ss1.invokeFactory('Survey Select Question', 'ssq1')
        self.failUnless('ssq1' in ss1.objectIds())
        ss1.invokeFactory('Survey Text Question', 'stq1')
        self.failUnless('stq1' in ss1.objectIds())
        #ss1.invokeFactory('Survey Two Dimensional', 'std1')
        #self.failUnless('std1' in ss1.objectIds())

    def testCreateSelectQuestion(self):
        self.s1.invokeFactory('Survey Select Question', 'sq1')
        self.failUnless('sq1' in self.s1.objectIds())
        
    def testEditSelectQuestion(self):
        self.s1.invokeFactory('Survey Select Question', 'sq1')
        sq1 = getattr(self.s1, 'sq1')

        sq1.setTitle('Select Question title')
        sq1.setDescription('Select Question description')

        self.assertEqual(sq1.Title(), 'Select Question title')
        self.assertEqual(sq1.Description(), 'Select Question description')

    def testCreateSurveyTextQuestion(self):
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        self.failUnless('stq1' in self.s1.objectIds())
        
    def testEditSurveyTextQuestion(self):
        self.s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(self.s1, 'stq1')

        stq1.setTitle('Question title')
        stq1.setDescription('Question description')
        stq1.setRequired(True)

        self.assertEqual(stq1.Title(), 'Question title')
        self.assertEqual(stq1.Description(), 'Question description')
        self.assertEqual(stq1.getRequired(), True)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    suite.addTest(makeSuite(TestContentCreation))
    return suite
