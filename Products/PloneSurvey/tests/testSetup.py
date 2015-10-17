import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions
from base import INTEGRATION_TESTING


class TestInstallation(unittest.TestCase):
    """Ensure product is properly installed"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.metaTypes = ('Survey',
                          'Sub Survey',
                          'Survey Date Question',
                          'Survey Matrix',
                          'Survey Matrix Question',
                          'Survey Select Question',
                          'Survey Text Question')

    def testCssInstalled(self):
        self.failUnless(
            '++resource++Products.PloneSurvey.stylesheets/survey_results.css'
            in self.portal.portal_css.getResourceIds())

    def testJsInstalled(self):
        self.failUnless(
            '++resource++Products.PloneSurvey.javascripts/survey_reset.js'
            in self.portal.portal_javascripts.getResourceIds())

    def testSkinLayersInstalled(self):
        self.failUnless('plone_survey' in self.portal.portal_skins.objectIds())

    def testPortalFactorySetup(self):
        self.failUnless('Survey' in
                        self.portal.portal_factory.getFactoryTypes())

    def testTypesInstalled(self):
        for t in self.metaTypes:
            self.failUnless(t in self.portal.portal_types.objectIds())

    def testTypesIdCorrect(self):
        """Ensure portal type id is correct for each type"""
        for t in self.metaTypes:
            assert t == self.portal.portal_types.getTypeInfo(t).id, t

    def testPortalTypesCorrect(self):
        """Ensure portal type is correct for each type"""
        for t in self.metaTypes:
            assert t == self.portal.portal_types.getTypeInfo(t).Title(), t

    def testMetaTypesCorrect(self):
        """Ensure meta type is correct for each type"""
        for t in self.metaTypes:
            assert t.replace(' ', '') == \
                self.portal.portal_types.getTypeInfo(t).content_meta_type, t

    def testMetaTypesNotToList(self):
        navtree_props = self.portal.portal_properties.navtree_properties
        metaTypesNotToList = navtree_props.metaTypesNotToList
        for t in self.metaTypes:
            if t not in ['Survey', 'Sub Survey']:
                self.failUnless(t in metaTypesNotToList)

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


class TestTypeProperties(unittest.TestCase):
    """Test properties of the types are correct"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.types = self.portal.portal_types
        self.archetype_tool = self.portal.archetype_tool

    def testSubSurvey(self):
        type_info = self.types.getTypeInfo('Sub Survey')
        assert type_info.Title() == 'Sub Survey'
        assert type_info.Metatype() == 'SubSurvey'
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.portal.s1.invokeFactory('Sub Survey', 'ss1')
        ss1 = getattr(self.portal.s1, 'ss1')
        assert ss1.meta_type == 'SubSurvey'
        assert ss1.portal_type == 'Sub Survey'
        archetype_info = self.archetype_tool.lookupType('Products.PloneSurvey',
                                                        'SubSurvey')
        assert archetype_info['portal_type'] == 'Sub Survey'
        assert archetype_info['meta_type'] == 'SubSurvey'
        assert archetype_info['name'] == 'SubSurvey'
        assert archetype_info['identifier'] == 'Subsurvey'


class TestContentCreation(unittest.TestCase):
    """Ensure content types can be created and edited"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')

    def testCreateSurvey(self):
        self.failUnless('s1' in self.portal.objectIds())

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


class TestTypeActions(unittest.TestCase):
    """Test the conditions on the type actions"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')

    def testSharingTab(self):
        s1 = getattr(self, 's1')
        action_tool = getToolByName(self.portal, 'portal_actions')
        actions = action_tool.listFilteredActionsFor(s1)
        sharing_tab_available = False
        for action in actions['object']:
            if action['id'] == 'local_roles':
                sharing_tab_available = True
        assert sharing_tab_available, "Sharing tab not available"

    def testSharingTabText(self):
        s1 = getattr(self, 's1')
        s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(s1, 'stq1')
        action_tool = getToolByName(self.portal, 'portal_actions')
        actions = action_tool.listFilteredActionsFor(stq1)
        sharing_tab_available = False
        for action in actions['object']:
            if action['id'] == 'local_roles':
                sharing_tab_available = True
        assert sharing_tab_available, "Sharing tab not available"


class TestAclUsers(unittest.TestCase):
    """Test acl_users is created"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')

    def testAclUsersCreated(self):
        s1 = getattr(self, 's1')
        s1.at_post_create_script()
        assert 'acl_users' in s1.objectIds(), "acl_users not created"
