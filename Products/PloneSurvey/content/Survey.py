import string
import csv

from cStringIO import StringIO
from DateTime import DateTime
from ZODB.POSException import ConflictError
#from zope.interface import implements

from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
# needed for getAnonymousID
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory

from Products.PluggableAuthService.PluggableAuthService import addPluggableAuthService
from Products.PlonePAS.Extensions.Install import *
from cStringIO import StringIO

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import SURVEY_STATUS, NOTIFICATION_METHOD, BARCHART_COLORS
#from Products.PloneSurvey.interfaces import ISurvey

schema = ATContentTypeSchema.copy() + ConstrainTypesMixinSchema + Schema((
    
    TextField('body',
        searchable = 1,
        required=0,
        schemata="Introduction",
        default_content_type    = 'text/html',
        default_output_type     = 'text/html',
        allowable_content_types=('text/plain',
                                 'text/structured',
                                 'text/html',
                                ),
        widget = RichWidget(description = "Enter an introduction for the survey.",
                            label = "Introduction",
                            label_msgid = 'label_introduction',
                            description_msgid = 'help_introduction',
                            rows = 5,
                            i18n_domain="plonesurvey",
                           ),
        ),

##    LinesField('dimensions',
##        searchable=0,
##        required=0,
##        default=[],
##        widget=LinesWidget(
##            label="Dimensions",
##            label_msgid="label_dimensions",
##            description="""Questions can be associated with one or more dimensions.
##                           Press enter to seperate the options.""",
##            description_msgid="help_dimensions",
##            i18n_domain="plonesurvey",),
##        ),

    TextField('thankYouMessage',
        required=0,
        searchable=0,
        default_method="translateThankYouMessage",
        widget=TextAreaWidget(
            label="'Thank you' message text",
            label_msgid="label_thank",
            description="""This is the message that will be displayed to the
                           user when they complete the survey.""",
            description_msgid="help_thankyou",
            i18n_domain="plonesurvey",
           ),
        ),

    TextField('savedMessage',
        required=0,
        searchable=0,
        default_method="translateSavedMessage",
        widget=TextAreaWidget(
            label="'Saved' message test",
            label_msgid="label_saved_text",
            description="""This is the message that will be displayed to the user
                           when they save the survey, but don't submit it.""",
            description_msgid="help_saved_text",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('exitUrl',
        required=0,
        searchable=0,
        widget=StringWidget(
            label="Exit URL",
            label_msgid="label_exit_url",
            description="""This is the URL that the user will be directed to on completion of the survey.
                           Use "http://site.to.go.to/page" or "route/to/page" for this portal""",
            description_msgid="help_exit_url",
            i18n_domain="plonesurvey",
          ),
        ),

    BooleanField('confidential',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Confidential",
            label_msgid="XXX",
            description="""Prevent respondents usernames from appearing in results""",
            description_msgid="XXX",
            i18n_domain="plonesurvey",
          ),
        ),

    BooleanField('allowAnonymous',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Allow Anonymous",
            label_msgid="label_allow_anonymous",
            i18n_domain="plonesurvey",
          ),
        ),

    BooleanField('allowSave',
        searchable=0,
        required=0,
        widget=BooleanWidget(
            label="Allow Save Functionality",
            label_msgid="label_allow_save",
            description="Allow logged in users to save survey for finishing later.",
            description_msgid="help_allow_save",
            i18n_domain="plonesurvey",
          ),
        ),

    StringField('surveyNotificationEmail',
        required=0,
        searchable=0,
        widget=StringWidget(
            label="Survey Notification Email Address",
            label_msgid="label_survey_notification_email",
            description="Enter an email address to receive notifications of survey completions.",
            description_msgid="help_survey_notification_email",
            i18n_domain="plonesurvey",
          ),
        ),

    StringField('surveyNotificationMethod',
        required=0,
        searchable=0,
        vocabulary=NOTIFICATION_METHOD,
        widget=SelectionWidget(
            label="Survey Notification Method",
            label_msgid="label_survey_notification_method",
            description="Select a method to receive notification emails.",
            description_msgid="help_survey_notification_method",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('completedFor',
        searchable=0,
        required=0,
        default=[],
        widget=StringWidget(visible=0,),
        ),

    ))

finalizeATCTSchema(schema, moveDiscussion=False)
schema["description"].widget.label = "Survey description"
schema["description"].widget.label_msgid = "label_description"
schema["description"].widget.description = "Add a short description of the survey here."
schema["description"].widget.description_msgid = "help_description"
schema["description"].widget.i18n_domain = "plonesurvey"
del schema["relatedItems"]

# Dumb class to work around bug in _getPropertyProviderForUser which
# causes it to always operate on portal.acl_users
class BasicPropertySheet:
    def __init__(self, sheet):
        self._properties = dict(sheet.propertyItems())

    def propertyItems(self):
        return self._properties.items()

    def setProperty(self, id, value):
        self._properties[id] = value

class Survey(ATCTOrderedFolder):
    """You can add questions to surveys"""
    schema = schema
    _at_rename_after_creation = True

    #implements(ISurvey)

    security = ClassSecurityInfo()

    def at_post_create_script(self):
        """Create PAS acl_users else login_form does not work"""
        # need Manager role to add an acl_users object
        remove_role = False
        if not getSecurityManager().checkPermission(permissions.ManagePortal, self):
            portal_membership = getToolByName(self, 'portal_membership')
            current_user = portal_membership.getAuthenticatedMember()
            current_userid = current_user.getId()
            self.manage_addLocalRoles(userid=current_userid, roles=['Manager',])
            remove_role = True
        # Re-use code in PlonePAS install
        addPluggableAuthService(self)
        io = StringIO()
        challenge_chooser_setup(self, io)
        registerPluginTypes(self.acl_users)
        setupPlugins(self, io)
        
        # Recreate mutable_properties but specify fields
        uf = self.acl_users
        pas = uf.manage_addProduct['PluggableAuthService']
        plone_pas = uf.manage_addProduct['PlonePAS']
        plone_pas.manage_delObjects('mutable_properties')
        plone_pas.manage_addZODBMutablePropertyProvider('mutable_properties',
            fullname='', key='')
        activatePluginInterfaces(self, 'mutable_properties', io)
        if remove_role:
            self.manage_delLocalRoles(userids=[current_userid,])

    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        """Doesn't make sense for surveys to allow alternate views"""
        return False

    security.declarePublic('canConstrainTypes')
    def canConstrainTypes(self):
        """Should not be able to add non survey types"""
        return False

    security.declareProtected(permissions.View, 'isMultipage')
    def isMultipage(self):
        """Return true if there is more than one page in the survey"""
        if self.getFolderContents(contentFilter={'portal_type':'Sub Survey',}):
            return True

    security.declareProtected(permissions.View, 'getQuestions')
    def getQuestions(self):
        """Return the questions for this part of the survey"""
        questions = self.getFolderContents(
            contentFilter={'portal_type':[
                'Survey Matrix',
                'Survey Select Question',
                'Survey Text Question',
                'Survey Two Dimensional',
                ]},
            full_objects=True)
        return questions

    security.declareProtected(permissions.View, 'getAllQuestions')
    def getAllQuestions(self):
        """Return all the questions in the survey"""
        portal_catalog = getToolByName(self, 'portal_catalog')
        questions = []
        path = string.join(self.getPhysicalPath(), '/')
        results = portal_catalog.searchResults(portal_type = ['Survey Matrix Question',
                                                              'Survey Select Question',
                                                              'Survey Text Question',
                                                              'Survey Two Dimensional',],
                                               path = path,
                                               order = 'getObjPositionInParent')
        for result in results:
            questions.append(result.getObject())
        return questions

    security.declareProtected(permissions.View, 'getAllQuestionsInOrder')
    def getAllQuestionsInOrder(self, include_sub_survey=False):
        """Return all the questions in the survey"""
        questions = []
        objects = self.getFolderContents(
            contentFilter={'portal_type':[
                'Sub Survey',
                'Survey Matrix',
                'Survey Select Question',
                'Survey Text Question',
                'Survey Two Dimensional',
                ]},
            full_objects=True)
        for object in objects:
            if object.portal_type == 'Sub Survey':
                if include_sub_survey:
                    questions.append(object)
                sub_survey_objects = object.getFolderContents(
                    contentFilter={'portal_type':[
                        'Survey Matrix',
                        'Survey Select Question',
                        'Survey Text Question',
                        'Survey Two Dimensional',
                        ]},
                    full_objects=True)
                for sub_survey_object in sub_survey_objects:
                    questions.append(sub_survey_object)
                    if sub_survey_object.portal_type == 'Survey Matrix':
                        survey_matrix_objects = sub_survey_object.getFolderContents(
                            contentFilter={'portal_type' : 'Survey Matrix Question'},
                            full_objects=True)
                        for survey_matrix_object in survey_matrix_objects:
                            questions.append(survey_matrix_object)
                    elif sub_survey_object.portal_type == 'Survey Two Dimensional':
                        survey_2d_objects = sub_survey_object.getFolderContents(
                            contentFilter={'portal_type' : 'Survey 2-Dimensional Question'},
                            full_objects=True)
                        for survey_2d_object in survey_2d_objects:
                            questions.append(survey_2d_object)
            elif object.portal_type == 'Survey Two Dimensional':
                questions.append(object)
                survey_2d_objects = object.getFolderContents(
                    contentFilter={'portal_type' : 'Survey 2-Dimensional Question'},
                    full_objects=True)
                for survey_2d_object in survey_2d_objects:
                    questions.append(survey_2d_object)
                # XXX should check if comment is present
            elif object.portal_type == 'Survey Matrix':
                questions.append(object)
                survey_matrix_objects = object.getFolderContents(
                    contentFilter={'portal_type' : 'Survey Matrix Question'},
                    full_objects=True)
                for survey_matrix_object in survey_matrix_objects:
                    questions.append(survey_matrix_object)
                # XXX should check if comment is present
            else:
                questions.append(object)
        return questions

    security.declareProtected(permissions.View, 'getNextPage')
    def getNextPage(self):
        """Return the next page of the survey"""
        pages = self.getFolderContents(contentFilter={'portal_type':'Sub Survey',}, full_objects=True)
        current_page = -1
        userid = self.getSurveyId()
        while 1==1:
            try:
                next_page = pages[current_page+1]
            except IndexError:
                # no next page, so survey finished
                self.setCompletedForUser()
                return self.exitSurvey()
            if next_page.getRequiredQuestion():
                question = next_page[next_page.getRequiredQuestion()]
                if next_page.getRequiredAnswerYesNo():
                    if question.getAnswerFor(userid) == next_page.getRequiredAnswer():
                        return next_page()
                else:
                    if question.getAnswerFor(userid) != next_page.getRequiredAnswer():
                        return next_page()
            else:
                return next_page()
            current_page += 1

    security.declareProtected(permissions.View, 'exitSurvey')
    def exitSurvey(self):
        """Return the defined exit url"""
        exit_url = self.getExitUrl()
        if exit_url[:4] != 'http':
            self.plone_utils.addPortalMessage(self.getThankYouMessage())
            exit_url = self.portal_url() + '/' + exit_url
        return self.REQUEST.RESPONSE.redirect(exit_url)

    security.declareProtected(permissions.View, 'saveSurvey')
    def saveSurvey(self):
        """Return the defined exit url"""
        exit_url = self.getExitUrl()
        if exit_url[:4] != 'http':
            self.plone_utils.addPortalMessage(self.getSavedMessage())
            exit_url = self.portal_url() + '/' + exit_url
        return self.REQUEST.RESPONSE.redirect(exit_url)

    security.declareProtected(permissions.View, 'setCompletedForUser')
    def setCompletedForUser(self):
        """Set completed for a user"""
        userid = self.getSurveyId()
        completed = self.getCompletedFor()
        completed.append(userid)
        self.setCompletedFor(completed)

        # Scramble respondent's password because we don't want him back
        acl_users = self.get_acl_users()
        user = acl_users.getUserById(userid)
        if user is not None:
            portal_registration = getToolByName(self, 'portal_registration')
            pw = portal_registration.generatePassword()
            
            self.acl_users.userFolderEditUser(userid, pw, user.getRoles(), user.getDomains(), key=pw)
            
            # Set key
            props = acl_users.mutable_properties.getPropertiesForUser(user)
            props = BasicPropertySheet(props)
            props.setProperty('key', pw)
            acl_users.mutable_properties.setPropertiesForUser(user, props)

        if self.getSurveyNotificationMethod() == 'each_submission':
            self.send_email(userid)

    security.declareProtected(permissions.View, 'checkCompletedFor')
    def checkCompletedFor(self, user_id):
        """Check whether a user has completed the survey"""
        completed = self.getCompletedFor()
        if user_id in completed:
            return True
        return False

    security.declareProtected(permissions.View, 'getSurveyId')
    def getSurveyId(self):
        """Return the userid for the survey"""
        portal_membership = getToolByName(self, 'portal_membership')
        if not portal_membership.isAnonymousUser():
            return portal_membership.getAuthenticatedMember().getId()
        request = self.REQUEST
        response = request.RESPONSE
        survey_cookie = self.getId()
        if self.getAllowAnonymous() and request.has_key(survey_cookie):
            return request.get(survey_cookie, "Anonymous")
        survey_id = self.getAnonymousId()
        #expires = (DateTime() + 365).toZone('GMT').rfc822() # cookie expires in 1 year (365 days)
        response.setCookie(survey_cookie, survey_id, path='/')
        return survey_id

    security.declareProtected(permissions.View, 'getAnonymousId')
    def getAnonymousId(self):
        """returns the id to use for an anonymous user"""
        portal_membership = getToolByName(self, 'portal_membership')
        if portal_membership.isAnonymousUser() and self.getAllowAnonymous():
            anon_id = 'Anonymous@'
            if not self.getConfidential():
                remote_ip = self.getRemoteIp()
                if remote_ip:
                    anon_id = anon_id + remote_ip + '@'
            return anon_id + str(DateTime())
        elif portal_membership.isAnonymousUser():
            return self.REQUEST.RESPONSE.redirect(self.portal_url()+'/login_form?came_from='+self.absolute_url())
        return portal_membership.getAuthenticatedMember().getId()

    security.declareProtected(permissions.View, 'getRemoteIp')
    def getRemoteIp(self):
        """returns the ip address of the survey respondent"""
        # XXX put in placeholder for working out the ip address
        return
        if self.getConfidential():
            return
        ip_address = self.REQUEST.environ['REMOTE_ADDR']
        if ip_address == "127.0.0.1":
            try:
                ip_address = self.REQUEST.environ['HTTP_X_FORWARDED_FOR']
            except KeyError:
                # might be using it on a localhost
                return
        return ip_address
        #return self.REQUEST.getClientAddr()
        #return self.REQUEST['REMOTE_ADDR']
        #return self.REQUEST['HTTP_X_FORWARDED_FOR']

    security.declareProtected(permissions.ModifyPortalContent, 'getRespondents')
    def getRespondents(self):
        """Return a list of respondents"""
        questions = self.getAllQuestionsInOrder()
        users = {}
        for question in questions:
            for user in question.answers.keys():
                users[user] = 1
        return users.keys()

    security.declareProtected(permissions.ModifyPortalContent, 'getRespondentFullName')
    def getRespondentFullName(self, userid):
        """get user. used by results spreadsheets to show fullname"""
        portal_membership = getToolByName(self, 'portal_membership')
        member = portal_membership.getMemberById(userid)
        if member is None:
            return
        full_name = member.getProperty('fullname')
        if full_name:
            return full_name
        return member.id

    security.declareProtected(permissions.ModifyPortalContent, 'getRespondents')
    def getAnswersByUser(self, userid):
        """Return a set of answers by user id"""
        questions = self.getAllQuestionsInOrder()
        answers = {}
        for question in questions:
            answer = question.getAnswerFor(userid)
            answers[question.getId()] = answer
        return answers

    security.declareProtected(permissions.View, 'getQuestionsCount')
    def getQuestionsCount(self):
        """Return a count of questions asked"""
        return len(self.questions)

    security.declareProtected(permissions.View, 'getSurveyColors')
    def getSurveyColors(self, num_options):
        """Return the colors for the barchart"""
        colors = BARCHART_COLORS
        num_colors = len(colors)
        while num_colors < num_options:
            colors = colors + colors
            num_colors = len(colors)
        return colors

    security.declareProtected(permissions.ResetOwnResponses,
                              'resetForAuthenticatedUser')
    def resetForAuthenticatedUser(self):
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        user_id = member.getMemberId()
        return self.resetForUser(user_id)

    security.declareProtected(permissions.ModifyPortalContent,
                              'resetForUser')
    def resetForUser(self, userid):
        """Remove answer for a single user"""
        completed = self.getCompletedFor()
        if userid in completed:
            completed.remove(userid)
        self.setCompletedFor(completed)
        questions = self.getAllQuestionsInOrder()
        for question in questions:
            question.resetForUser(userid)

    security.declareProtected(permissions.View, 'send_email')
    def send_email(self, userid):
        """ Send email to nominated address """
        properties = self.portal_properties.site_properties
        mTo = self.getSurveyNotificationEmail()
        mFrom = properties.email_from_address
        mSubj = '[%s] New survey submitted' % self.Title()
        message = []
        message.append('Survey %s.' % self.Title())
        message.append('has been completed by user: %s.' % userid)
        message.append(self.absolute_url() + '/survey_view_results')
        mMsg = '\n\n'.join(message)
        try:
            self.MailHost.send(mMsg, mTo, mFrom, mSubj)
        except ConflictError:
            raise
        except:
            # XXX too many things can go wrong
            pass

    security.declarePublic('translateThankYouMessage')
    def translateThankYouMessage(self):
        """ """
        return self.translate(msgid="text_default_thank_you",
                              default="Thank you for completing the survey.",
                              domain="plonesurvey")

    security.declarePublic('translateSavedMessage')
    def translateSavedMessage(self):
        """ """
        return self.translate(msgid="text_default_saved_message",
                              default="You have saved the survey.\nDon't forget to come back and finish it.",
                              domain="plonesurvey")

    security.declareProtected(permissions.ModifyPortalContent, 'deleteAuthenticatedRespondent')
    def deleteAuthenticatedRespondent(self, email, REQUEST=None):
        """Delete authenticated respondent"""
        # xxx: delete answers by this user as well?
        self.get_acl_users().userFolderDelUsers([email])
        if REQUEST is not None:
            pu = getToolByName(self, 'plone_utils')
            pu.addPortalMessage("Respondent %s deleted" % email)
            REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)

    security.declareProtected(permissions.ModifyPortalContent, 'addAuthenticatedRespondent')
    def addAuthenticatedRespondent(self, emailaddress, **kw):
        acl_users = self.get_acl_users()
        portal_registration = getToolByName(self, 'portal_registration')
        
        # Create user
        password = portal_registration.generatePassword()
        acl_users.userFolderAddUser(emailaddress, password, roles=['Member'], domains=[],
            groups=())
        
        # Set user properties
        user = acl_users.getUserById(emailaddress)
        props = acl_users.mutable_properties.getPropertiesForUser(user)
        props = BasicPropertySheet(props)
        for k,v in kw.items():
            props.setProperty(k, v)
        props.setProperty('key', password)
        acl_users.mutable_properties.setPropertiesForUser(user, props)

    security.declareProtected(permissions.ModifyPortalContent, 'getAuthenticatedRespondent')
    def getAuthenticatedRespondent(self, emailaddress):
        """
        Return dictionary with respondent details. This method is needed because
        getProperty is hosed on the user object.
        """
        di = {'emailaddress':emailaddress, 'id':emailaddress}
        acl_users = self.get_acl_users()
        user = acl_users.getUserById(emailaddress)
        props = user.getPropertysheet('mutable_properties')
        for k,v in props.propertyItems():
            di[k] = v
        return di

    security.declareProtected(permissions.ModifyPortalContent, 'getAuthenticatedRespondents')
    def getAuthenticatedRespondents(self):
        return [self.getAuthenticatedRespondent(id) for id in self.get_acl_users().getUserNames()]
    
    def get_acl_users(self):
        """Fetch acl_users. Create if it does not yet exist."""
        if not 'acl_users' in self.objectIds():
            self.at_post_create_script()
        return self.acl_users

    security.declareProtected(permissions.View, 'buildSpreadsheetUrl')
    def buildSpreadsheetUrl(self):
        """Create a filename for the spreadsheets"""
        date = DateTime().strftime("%Y-%m-%d")
        id = self.getId()
        id = "%s-%s" % (id, date)
        url = "%s.csv" % id
        return url

    security.declareProtected(permissions.ModifyPortalContent, 'buildSpreadsheet2')
    def buildSpreadsheet2(self):
        """Build spreadsheet 2."""
        data = StringIO()
        sheet = csv.writer(data)
        questions = self.getAllQuestionsInOrder()
        
        sheet.writerow(('user',) + tuple(q.Title() for q in questions) + ('completed',))
        
        for user in self.getRespondents():
            if self.getConfidential():
                row = ['Anonymous']
            else:
                row = [self.getRespondentFullName(user) or user]
            for question in questions:
                answer = question.getAnswerFor(user) or ''
                # handle there being no answer (e.g branched question)
                if answer:
                    if not (isinstance(answer, str) or isinstance(answer, int)):
                        # It's a sequence, filter out empty values
                        answer = ', '.join(filter(None, answer))
                row.append(answer)
            
            row.append(self.checkCompletedFor(user) and 'Completed' or 'Not Completed')
            
            sheet.writerow(row)
        
        return data.getvalue()

    security.declareProtected(permissions.ModifyPortalContent, 'buildSpreadsheet3')
    def buildSpreadsheet3(self):
        """Build spreadsheet 3."""
        data = StringIO()
        sheet = csv.writer(data)
        questions = self.get_all_questions_in_order_filtered(ignore_meta_types=['SurveyTwoDimensional','SurveyMatrix'])
        sheet.writerow(('user',) + tuple(q.Title() for q in questions) + ('completed',))
        for user in self.getRespondents():
            row = [self.getRespondentFullName(user) or 'Anonymous']
            for question in questions:
                answer = ""
                if question.getInputType() in ['text', 'area']:
                    if question.getAnswerFor(user):
                        answer = '"' + question.getAnswerFor(user).replace('"',"'") + '"'
                    else:
                        answer = ""
                elif question.getInputType() in ['checkbox', 'multipleSelect']:
                    options = question.getQuestionOptions()
                    answerList = question.getAnswerFor(user)
                    if answerList and not isinstance(answerList, str):
                        for option in options:
                            if answerList.count(option) > 0:
                                answer += '1;'
                            else:
                                answer += '0;'
                        answer = '"' + answer[0:len(answer)-1] + '"'
                    elif answerList:
                        answer = '"' + answerList + '"'
                    else:
                        answer = ''
                else:
                    options = question.getQuestionOptions()
                    answerLabel = question.getAnswerFor(user)
                    answer = str(len(options))
                    i = 0
                    while i < len(options):
                        if options[i] == answerLabel:
                            answer = str(i)
                            break
                        i = i + 1
                row.append(answer)
#                if question.getCommentType():
#                line.append('"' + test(question.getCommentsFor(user), question.getCommentsFor(user).replace('"',"'"), "Blank") + '"')
            row.append(self.checkCompletedFor(user) and 'Completed' or 'Not Completed')
            sheet.writerow(row)
        return data.getvalue()

    security.declareProtected(permissions.ModifyPortalContent, 'buildSummarySpreadsheet')
    def buildSummarySpreadsheet(self):
        """Build the summary spreadsheet."""
        data = StringIO()
        sheet = csv.writer(data)
        questions = self.getAllQuestionsInOrder()
        for question in questions:
            row = [question.Title()]
            sheet.writerow(row)
        return data.getvalue()

    security.declareProtected(permissions.ManagePortal, 'fixSurveyResults')
    def should_be_integer(self):
        """Fix survey results"""
        return # XXX this method does not work yet
        questions = self.getAllQuestions()
        for question in questions:
            if question in ['Survey Matrix Question', 'Survey Select Question']:
                should_be_integer = question.getLikertOptions() and True or False
                raise str(should_be_integer)
                answers = question.answers
        return 'done'

registerType(Survey)
