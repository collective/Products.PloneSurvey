import string
import csv
from Products.CMFPlone.utils import safe_unicode

from cStringIO import StringIO
from DateTime import DateTime
from ZODB.POSException import ConflictError
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory

from Products.PluggableAuthService.PluggableAuthService import addPluggableAuthService
from Products.PlonePAS.Extensions.Install import *

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.config import BARCHART_COLORS
from Products.PloneSurvey.interfaces import ISurvey

from schemata import SurveySchema

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
    schema = SurveySchema
    _at_rename_after_creation = True

    implements(ISurvey)

    security = ClassSecurityInfo()

    def __init__(self, oid, **kwargs):
        self.reset()
        ATCTOrderedFolder.__init__(self, oid, **kwargs)

    security.declareProtected(permissions.ModifyPortalContent, 'reset')
    def reset(self):
        """Remove all respondents."""
        self.respondents = OOBTree()

    security.declarePrivate('createLocalPas')
    def createLocalPas(self):
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
                'Survey Date Question',
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
        results = portal_catalog.searchResults(portal_type = ['Survey Date Question',
                                                              'Survey Matrix Question',
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
                'Survey Date Question',
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
                        'Survey Date Question',
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

    security.declareProtected(permissions.View, 'getAllSelectQuestionsInOrder')
    def getAllSelectQuestionsInOrder(self):
        """Return all the vocab driven questions in the survey"""
        questions = []
        objects = self.getFolderContents(
            contentFilter={'portal_type':[
                'Sub Survey',
                'Survey Matrix',
                'Survey Select Question',
                ]},
            full_objects=True)
        for object in objects:
            if object.portal_type == 'Sub Survey':
                sub_survey_objects = object.getFolderContents(
                    contentFilter={'portal_type':[
                        'Survey Matrix',
                        'Survey Select Question',
                        ]},
                    full_objects=True)
                for sub_survey_object in sub_survey_objects:
                    if sub_survey_object.portal_type == 'Survey Matrix':
                        survey_matrix_objects = sub_survey_object.getFolderContents(
                            contentFilter={'portal_type' : 'Survey Matrix Question'},
                            full_objects=True)
                        for survey_matrix_object in survey_matrix_objects:
                            questions.append(survey_matrix_object)
                    else:
                        questions.append(sub_survey_object)
            elif object.portal_type == 'Survey Matrix':
                survey_matrix_objects = object.getFolderContents(
                    contentFilter={'portal_type' : 'Survey Matrix Question'},
                    full_objects=True)
                for survey_matrix_object in survey_matrix_objects:
                    questions.append(survey_matrix_object)
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
        self.setCompletedForUser()
        exit_url = self.getExitUrl()
        if exit_url[:4] != 'http':
            self.plone_utils.addPortalMessage(
                safe_unicode(self.getThankYouMessage()))
            exit_url = self.portal_url() + '/' + exit_url
        return self.REQUEST.RESPONSE.redirect(exit_url)

    security.declareProtected(permissions.View, 'saveSurvey')
    def saveSurvey(self):
        """Return the defined exit url"""
        exit_url = self.getExitUrl()
        if exit_url[:4] != 'http':
            self.plone_utils.addPortalMessage(
                safe_unicode(self.getSavedMessage()))
            exit_url = self.portal_url() + '/' + exit_url
        return self.REQUEST.RESPONSE.redirect(exit_url)

    security.declareProtected(permissions.View, 'setCompletedForUser')
    def setCompletedForUser(self):
        """Set completed for a user"""
        userid = self.getSurveyId()
        respondents = self.respondents
        respondents[userid]['end'] = DateTime()
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
        request = self.REQUEST
        # Check the request for saving questions on the first survey page
        try:
            user_id = request.form['survey_user_id']
        except KeyError:
            pass
        else:
            return user_id
        portal_membership = getToolByName(self, 'portal_membership')
        if not portal_membership.isAnonymousUser():
            user_id = portal_membership.getAuthenticatedMember().getId()
            self.addRespondent(user_id)
            return user_id
        response = request.RESPONSE
        survey_cookie = self.getId()
        if self.getAllowAnonymous() and request.has_key(survey_cookie):
            return request.get(survey_cookie, "Anonymous")
        user_id = self.getAnonymousId()
        #expires = (DateTime() + 365).toZone('GMT').rfc822() # cookie expires in 1 year (365 days)
        response.setCookie(survey_cookie, user_id, path='/')
        self.addRespondent(user_id)
        return user_id

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
    def getRemoteIp(self, request=None):
        """returns the ip address of the survey respondent"""
        # XXX put in placeholder for working out the ip address
        if self.getConfidential():
            return
        if request is None:
            request = getattr(self, 'REQUEST', None)
        return request.getClientAddr()
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

    security.declareProtected(permissions.ModifyPortalContent, 'getRespondentsDetails')
    def getRespondentsDetails(self):
        """Return a list of respondents details"""
        # TODO needs moving to an event handler
        try:
            respondents = self.respondents
        except AttributeError:
            self.reset()
        return self.respondents

    security.declareProtected(permissions.ModifyPortalContent, 'getRespondentsList')
    def getRespondentsList(self):
        """Return a list of respondents details"""
        users = {}
        for user in self.respondents.keys():
            users[user] = 1
        return users.keys()

    security.declareProtected(permissions.ModifyPortalContent, 'getRespondentDetails')
    def getRespondentDetails(self, respondent):
        """Return details of a respondent"""
        try:
            respondents = self.respondents
        except AttributeError:
            self.reset()
        try:
            details = self.respondents[respondent]
        except KeyError:
            # TODO try/except should be removed at some point
            # probably old survey, create respondent details
            if respondent.find('@'):
                saved_details = respondent.split('@')
            #saved_details = respondent.split('@')
            self.respondents[respondent] = PersistentMapping(start='',
                                                             ip_address='',
                                                             end='')
        details_dict = {}
        details = self.respondents[respondent]
        for k in details.keys():
            details_dict[k] = details[k]
        return details_dict

    security.declareProtected(permissions.ModifyPortalContent, 'addRespondent')
    def addRespondent(self, user_id):
        """Add a respondent to the survey"""
        # TODO needs moving to an event handler
        try:
            respondents = self.respondents
        except AttributeError:
            self.reset()
        self.respondents[user_id] = PersistentMapping(start=DateTime(),
                                                      ip_address=self.getRemoteIp(),
                                                      end='')

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
        # XXX is this used anywhere?
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
        try:
            if self.respondents.has_key(userid):
                del self.respondents[userid]
        except AttributeError:
            # TODO old survey instance
            self.reset()

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
            pu.addPortalMessage(
                safe_unicode("Respondent %s deleted" % email))
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
            self.createLocalPas()
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
        row = ['Question', 'Option', 'Number of Responses', 'Percentage']
        sheet.writerow(row)
        questions = self.getAllQuestionsInOrder()
        for question in questions:
            row = [question.Title(), '']
            row.append(question.getNumberOfRespondents())
            sheet.writerow(row)
            if question.portal_type in ['Survey Select Question','Survey Matrix Question']:
                options = question.getQuestionOptions()
                number_options = question.getAggregateAnswers()
                percentage_options = question.getPercentageAnswers()
                for option in options:
                    row = ['', option]
                    row.append(number_options[option])
                    row.append(percentage_options[option])
                    sheet.writerow(row)
        return data.getvalue()

    security.declareProtected(permissions.ModifyPortalContent, 'buildSelectSpreadsheet')
    def buildSelectSpreadsheet(self, boolean=False):
        """Build the select spreadsheet."""
        data = StringIO()
        sheet = csv.writer(data)
        questions = self.getAllSelectQuestionsInOrder()
        row = ['user',]
        options_row = ['',]
        for question in questions:
            options = question.getQuestionOptions()
            for i in range(len(options)):
                if i == 0:
                    row.append(question.Title())
                else:
                    row.append('')
                options_row.append(options[i])
        sheet.writerow(row)
        sheet.writerow(options_row)
        for user in self.getRespondents():
            if self.getConfidential():
                row = ['Anonymous']
            else:
                row = [self.getRespondentFullName(user) or user]
            for question in questions:
                options = question.getQuestionOptions()
                answer = question.getAnswerFor(user)
                for i in range(len(options)):
                    if answer is None:
                        if boolean:
                            row.append(0)
                        else:
                            row.append('')
                    else:
                        if options[i] in answer:
                            if boolean:
                                row.append(1)
                            else:
                                row.append(options[i])
                        else:
                            if boolean:
                                row.append(0)
                            else:
                                row.append('')
            row.append(self.checkCompletedFor(user) and 'Completed' or 'Not Completed')
            sheet.writerow(row)
        return data.getvalue()

    security.declareProtected(permissions.ManagePortal, 'fixSurveyResults')
    def fixSurveyResults(self):
        """Fix survey results"""
        return # XXX this method does not work yet
        questions = self.getAllQuestions()
        for question in questions:
            if question in ['Survey Matrix Question', 'Survey Select Question']:
                should_be_integer = question.getLikertOptions() and True or False
                raise str(should_be_integer)
                answers = question.answers
        return 'done'

    security.declareProtected(permissions.View, 'checkPloneVersion')
    def checkPloneVersion(self):
        """Check if we are on Plone 2.5"""
        # TODO for Plone 3.0, can be removed once sharing and properties actions on types removed
        migration_tool = getToolByName(self, 'portal_migration')
        plone_version = migration_tool.getInstanceVersion()
        if plone_version[:3] == '2.5':
            return True
        return False

registerATCT(Survey, PROJECTNAME)

def createSurveyEventHandler(ob, event):
    """Initialise the survey"""
    if not 'acl_users' in ob.objectIds():
        ob.createLocalPas()
