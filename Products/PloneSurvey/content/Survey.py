import string
import csv
import os
import transaction
import urllib
from Products.CMFPlone.utils import safe_unicode

from cStringIO import StringIO
from DateTime import DateTime
from ZODB.POSException import ConflictError
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping
from zope.i18n import translate

from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.utils import DT2dt
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.exceptions import BadRequest

from Products.PluggableAuthService.PluggableAuthService \
    import addPluggableAuthService
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from Products.PlonePAS.setuphandlers import challenge_chooser_setup
from Products.PlonePAS.setuphandlers import registerPluginTypes
from Products.PlonePAS.setuphandlers import setupPlugins

from Products.PloneSurvey import PloneSurveyMessageFactory as _
from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.config import BARCHART_COLORS
from Products.PloneSurvey.interfaces.survey import ISurvey
from Products.PloneSurvey.config import DEFAULT_SURVEY_INVITE
from Products.PloneSurvey.permissions import ResetOwnResponses
from Products.PloneSurvey.permissions import ViewSurveyResults

from schemata import SurveySchema

try:
    from collective.recaptcha.settings import getRecaptchaSettings
    using_collective_recaptcha = True
except ImportError:
    using_collective_recaptcha = False


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

    security.declareProtected(permissions.ModifyPortalContent, 'reset')

    def reset(self):
        """Remove all respondents."""
        self.respondents = OOBTree()

    def _checkId(self, id, allow_dup=0):
        """Bypass the root object check for the local acl_users"""
        try:
            return super(Survey, self)._checkId(id, allow_dup=0)
        except BadRequest:
            if id != 'acl_users':
                raise

    security.declarePrivate('createLocalPas')

    def createLocalPas(self):
        """Create PAS acl_users else login_form does not work"""
        # need Manager role to add an acl_users object
        remove_role = False
        if not getSecurityManager().checkPermission(permissions.ManagePortal,
                                                    self):
            portal_membership = getToolByName(self, 'portal_membership')
            current_user = portal_membership.getAuthenticatedMember()
            current_userid = current_user.getId()
            self.manage_addLocalRoles(userid=current_userid,
                                      roles=['Manager', ])
            remove_role = True
        # Re-use code in PlonePAS install
        addPluggableAuthService(self)
        out = StringIO()
        try:
            challenge_chooser_setup(self)
        except TypeError:
            # BBB needed for Plone 3.3.5
            challenge_chooser_setup(self, out)
        registerPluginTypes(self.acl_users)
        try:
            setupPlugins(self)
        except TypeError:
            # BBB needed for Plone 3.3.5
            setupPlugins(self, out)

        # Recreate mutable_properties but specify fields
        uf = self.acl_users
        uf.manage_addProduct['PluggableAuthService']
        plone_pas = uf.manage_addProduct['PlonePAS']
        plone_pas.manage_delObjects('mutable_properties')
        plone_pas.manage_addZODBMutablePropertyProvider(
            'mutable_properties',
            fullname='',
            key='',
            email_sent='')
        activatePluginInterfaces(self, 'mutable_properties', out)
        if remove_role:
            self.manage_delLocalRoles(userids=[current_userid, ])

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
        if self.getFolderContents(contentFilter={'portal_type': 'Sub Survey'}):
            return True

    security.declareProtected(permissions.View, 'getQuestions')

    def getQuestions(self):
        """Return the questions for this part of the survey"""
        questions = self.getFolderContents(
            contentFilter={'portal_type': [
                'Survey Date Question',
                'Survey Matrix',
                'Survey Select Question',
                'Survey Text Question',
                ]},
            full_objects=True)
        return questions

    security.declareProtected(permissions.View, 'getAllQuestions')

    def getAllQuestions(self):
        """Return all the questions in the survey"""
        portal_catalog = getToolByName(self, 'portal_catalog')
        questions = []
        path = string.join(self.getPhysicalPath(), '/')
        results = portal_catalog.searchResults(
            portal_type=[
                'Survey Date Question',
                'Survey Matrix Question',
                'Survey Select Question',
                'Survey Text Question'
            ],
            path=path,
            order='getObjPositionInParent'
        )
        for result in results:
            questions.append(result.getObject())
        return questions

    security.declareProtected(permissions.View, 'getAllQuestionsInOrder')

    def getAllQuestionsInOrder(self, include_sub_survey=False):
        """Return all the questions in the survey"""
        questions = []
        objects = self.getFolderContents(
            contentFilter={'portal_type': [
                'Sub Survey',
                'Survey Date Question',
                'Survey Matrix',
                'Survey Select Question',
                'Survey Text Question',
                ]},
            full_objects=True)
        for object in objects:
            if object.portal_type == 'Sub Survey':
                if include_sub_survey:
                    questions.append(object)
                sub_survey_objects = object.getFolderContents(
                    contentFilter={'portal_type': [
                        'Survey Matrix',
                        'Survey Date Question',
                        'Survey Select Question',
                        'Survey Text Question',
                        ]},
                    full_objects=True)
                for sub_survey_object in sub_survey_objects:
                    questions.append(sub_survey_object)
                    if sub_survey_object.portal_type == 'Survey Matrix':
                        survey_matrix_objects = sub_survey_object.getFolderContents(
                            contentFilter={'portal_type': 'Survey Matrix Question'},
                            full_objects=True)
                        for survey_matrix_object in survey_matrix_objects:
                            questions.append(survey_matrix_object)
            elif object.portal_type == 'Survey Matrix':
                questions.append(object)
                survey_matrix_objects = object.getFolderContents(
                    contentFilter={'portal_type': 'Survey Matrix Question'},
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
            contentFilter={'portal_type': [
                'Sub Survey',
                'Survey Matrix',
                'Survey Select Question',
                ]},
            full_objects=True)
        for object in objects:
            if object.portal_type == 'Sub Survey':
                sub_survey_objects = object.getFolderContents(
                    contentFilter={'portal_type': [
                        'Survey Matrix',
                        'Survey Select Question',
                        ]},
                    full_objects=True)
                for sub_survey_object in sub_survey_objects:
                    if sub_survey_object.portal_type == 'Survey Matrix':
                        survey_matrix_objects = sub_survey_object.getFolderContents(
                            contentFilter={'portal_type': 'Survey Matrix Question'},
                            full_objects=True)
                        for survey_matrix_object in survey_matrix_objects:
                            questions.append(survey_matrix_object)
                    else:
                        questions.append(sub_survey_object)
            elif object.portal_type == 'Survey Matrix':
                survey_matrix_objects = object.getFolderContents(
                    contentFilter={'portal_type': 'Survey Matrix Question'},
                    full_objects=True)
                for survey_matrix_object in survey_matrix_objects:
                    questions.append(survey_matrix_object)
            else:
                questions.append(object)
        return questions

    security.declareProtected(permissions.View, 'hasDateQuestion')

    def hasDateQuestion(self):
        """Return true if there is a date question in this part of the survey
        to import the js"""
        objects = self.getFolderContents(
            contentFilter={'portal_type': 'Survey Date Question'})
        if objects:
            return True
        return False

    security.declareProtected(permissions.View, 'getNextPage')

    def getNextPage(self):
        """Return the next page of the survey"""
        pages = self.getFolderContents(
            contentFilter={'portal_type': 'Sub Survey', }, full_objects=True)
        for page in pages:
            if page.displaySubSurvey():
                return page()
        return self.exitSurvey()

    security.declareProtected(permissions.View, 'hasMorePages')

    def hasMorePages(self):
        """Return True if survey has more pages to display"""
        pages = self.getFolderContents(
            contentFilter={'portal_type': 'Sub Survey', }, full_objects=True)
        if not pages:
            return False
        return True

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

            self.acl_users.userFolderEditUser(
                userid,
                pw,
                user.getRoles(),
                user.getDomains(),
                key=pw)

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
        if self.getAllowAnonymous() and survey_cookie in request:
            return request.get(survey_cookie, "Anonymous")
        user_id = self.getAnonymousId()
        # expires = (DateTime() + 365).toZone('GMT').rfc822()
        # cookie expires in 1 year (365 days)
        response.setCookie(survey_cookie, user_id, path='/')
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
            return self.REQUEST.RESPONSE.redirect(
                self.portal_url() + '/login_form?came_from=' + self.absolute_url())
        return portal_membership.getAuthenticatedMember().getId()

    security.declareProtected(permissions.View, 'getRemoteIp')

    def getRemoteIp(self, request=None):
        """returns the ip address of the survey respondent"""
        if self.getConfidential():
            return
        if request is None:
            request = getattr(self, 'REQUEST', None)
        return request.getClientAddr()

    security.declareProtected(permissions.ModifyPortalContent,
                              'getRespondentsDetails')

    def getRespondentsDetails(self):
        """Return a list of respondents details"""
        return self.respondents

    security.declareProtected(permissions.ModifyPortalContent,
                              'getRespondentsList')

    def getRespondentsList(self):
        """Return a list of respondents details"""
        users = {}
        for user in self.respondents.keys():
            users[user] = 1
        return users.keys()

    security.declareProtected(ViewSurveyResults, 'getRespondentDetails')

    def getRespondentDetails(self, respondent):
        """Return details of a respondent"""
        try:
            self.respondents
        except AttributeError:
            self.reset()
        try:
            details = self.respondents[respondent]
        except KeyError:
            # TODO try/except should be removed at some point
            # probably old survey, create respondent details
            self.respondents[respondent] = PersistentMapping(start='',
                                                             ip_address='',
                                                             end='')
        details_dict = {}
        details = self.respondents[respondent]
        for k in details.keys():
            details_dict[k] = details[k]
        if details['start'] and details['end']:
            details_dict['time_taken'] = DT2dt(details['end']) - DT2dt(details['start'])
        else:
            details_dict['time_taken'] = ''
        return details_dict

    security.declareProtected(permissions.ModifyPortalContent, 'addRespondent')

    def addRespondent(self, user_id):
        """Add a respondent to the survey"""
        # TODO needs moving to an event handler
        try:
            self.respondents
        except AttributeError:
            self.reset()
        if user_id in self.respondents:
            return
        self.respondents[user_id] = PersistentMapping(
            start=DateTime(),
            ip_address=self.getRemoteIp(),
            end='')

    security.declareProtected(ViewSurveyResults, 'getRespondentFullName')

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

    security.declareProtected(ViewSurveyResults, 'getAnswersByUser')

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

    security.declareProtected(ResetOwnResponses, 'resetForAuthenticatedUser')

    def resetForAuthenticatedUser(self):
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        user_id = member.getMemberId()
        return self._resetForUser(user_id)

    security.declareProtected(permissions.ModifyPortalContent,
                              'resetForUser')

    def resetForUser(self, userid):
        """Remove answer for a single user"""
        self._resetForUser(userid)

    def _resetForUser(self, userid):
        """Remove answer for a single user"""
        completed = self.getCompletedFor()
        if userid in completed:
            completed.remove(userid)
        self.setCompletedFor(completed)
        questions = self.getAllQuestionsInOrder()
        for question in questions:
            question.resetForUser(userid)
        try:
            if userid in self.respondents:
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
        mSubj = translate(_(
            '[${survey_title}] New survey submitted',
            mapping={'survey_title': safe_unicode(self.Title())}),
            context=self.REQUEST)
        message = []
        message.append(translate(_(
            'Survey ${survey_title}',
            mapping={'survey_title': safe_unicode(self.Title())}),
            context=self.REQUEST))
        message.append(translate(_(
            'has been completed by user: ${userid}',
            mapping={'userid': userid}),
            context=self.REQUEST))
        message.append(self.absolute_url() +
                       '/@@Products.PloneSurvey.survey_view_results')
        mMsg = '\n\n'.join(message)
        try:
            self.MailHost.send(mMsg, mTo, mFrom, mSubj, charset='utf-8')
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
        return self.translate(
            msgid="text_default_saved_message",
            default=u"You have saved the survey.\n "
                    u"Don't forget to come back and finish it.",
            domain="plonesurvey")

    security.declareProtected(permissions.ModifyPortalContent,
                              'deleteAuthenticatedRespondent')

    def deleteAuthenticatedRespondent(self, email, REQUEST=None):
        """Delete authenticated respondent"""
        # xxx: delete answers by this user as well?
        acl_users = self.get_acl_users()
        user = acl_users.getUserById(email)
        props = acl_users.mutable_properties.getPropertiesForUser(user)
        props = BasicPropertySheet(props)
        for prop in props.propertyItems():
            props.setProperty(prop[0], '')
        acl_users.mutable_properties.setPropertiesForUser(user, props)
        acl_users.userFolderDelUsers([email])
        if REQUEST is not None:
            pu = getToolByName(self, 'plone_utils')
            pu.addPortalMessage(
                safe_unicode("Respondent %s deleted" % email))
            REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)

    security.declareProtected(permissions.ModifyPortalContent,
                              'addAuthenticatedRespondent')

    def addAuthenticatedRespondent(self, emailaddress, **kw):
        acl_users = self.get_acl_users()
        portal_registration = getToolByName(self, 'portal_registration')
        if not emailaddress:
            return False
        # Create user
        password = portal_registration.generatePassword()
        acl_users.userFolderAddUser(
            emailaddress,
            password,
            roles=['Member'],
            domains=[],
            groups=())
        # Set user properties
        user = acl_users.getUserById(emailaddress)
        props = acl_users.mutable_properties.getPropertiesForUser(user)
        props = BasicPropertySheet(props)
        for k, v in kw.items():
            props.setProperty(k, v)
        props.setProperty('key', password)
        acl_users.mutable_properties.setPropertiesForUser(user, props)
        return True

    security.declareProtected(permissions.ModifyPortalContent,
                              'registerRespondentSent')

    def registerRespondentSent(self, email_address):
        """Mark the respondent as being sent an email"""
        acl_users = self.get_acl_users()
        user = acl_users.getUserById(email_address)
        props = acl_users.mutable_properties.getPropertiesForUser(user)
        props = BasicPropertySheet(props)
        props.setProperty('email_sent', str(DateTime()))
        acl_users.mutable_properties.setPropertiesForUser(user, props)

    security.declareProtected(permissions.ModifyPortalContent,
                              'getAuthenticatedRespondent')

    def getAuthenticatedRespondent(self, emailaddress):
        """
        Return dictionary with respondent details.
        This method is needed because
        getProperty is hosed on the user object.
        """
        di = {'emailaddress': emailaddress, 'id': emailaddress}
        acl_users = self.get_acl_users()
        user = acl_users.getUserById(emailaddress)
        props = user.getPropertysheet('mutable_properties')
        for k, v in props.propertyItems():
            di[k] = v
        return di

    security.declareProtected(permissions.ModifyPortalContent,
                              'getAuthenticatedRespondents')

    def getAuthenticatedRespondents(self):
        """Build up the list of users"""
        respondents = []
        users = self.get_acl_users().getUsers()
        for user in users:
            respondents.append(user.getId())
        return [self.getAuthenticatedRespondent(user_id)
                for user_id in respondents]

    security.declareProtected(permissions.ModifyPortalContent,
                              'sendSurveyInvite')

    def sendSurveyInvite(self, email_address):
        """Send a survey Invite"""
        portal_properties = getToolByName(self, 'portal_properties')
        acl_users = self.get_acl_users()
        user = acl_users.getUserById(email_address)
        user_details = self.getAuthenticatedRespondent(email_address)
        email_from_name = self.getInviteFromName()
        if not email_from_name:
            email_from_name = self.email_from_name
        email_from_address = self.getInviteFromEmail()
        if not email_from_address:
            email_from_address = self.email_from_address
        email_body = self.getEmailInvite()
        email_body = email_body.replace('**Name**', user_details['fullname'])
        survey_url = self.absolute_url() + '/login_form_bridge?email=' + \
            email_address + '&amp;key=' + urllib.quote(user_details['key'])
        email_body = email_body.replace(
            '**Survey**',
            '<a href="' + survey_url + '">' + self.Title() + '</a>')
        mail_text = self.survey_send_invite_template(
            user=user,
            email_body=email_body,
            subject=self.title_or_id())
        host = self.MailHost
        site_props = portal_properties.site_properties
        charset = site_props.default_charset or 'utf-8'
        mail_text = safe_unicode(mail_text)
        host.send(mail_text,
                  mto=user.getId(),
                  mfrom=u"{} <{}>".format(
                        safe_unicode(email_from_name), email_from_address),
                  subject=safe_unicode(self.title_or_id()),
                  charset=charset,
                  msg_type='text/html')
        self.registerRespondentSent(email_address)

    security.declareProtected(permissions.ModifyPortalContent,
                              'sendSurveyInviteAll')

    def sendSurveyInviteAll(self, send_to_all=False, use_transactions=False):
        """Send survey Invites to all respondents"""
        number_sent = 0
        if use_transactions:
            transaction.abort()
        respondents = self.acl_users.getUsers()
        already_completed = self.getRespondentsList()
        for respondent in respondents:
            if use_transactions:
                transaction.get()
            email_address = respondent.getId()
            respondent_details = self.getAuthenticatedRespondent(email_address)
            if email_address in already_completed:
                # don't send out an invite if already responded
                continue
            if not send_to_all:
                # don't send an email if one already sent
                if respondent_details['email_sent']:
                    continue
            self.sendSurveyInvite(email_address)
            number_sent += 1
        # return number of invites sent
        return number_sent

    def get_acl_users(self):
        """Fetch acl_users. Create if it does not yet exist."""
        if 'acl_users' not in self.objectIds():
            self.createLocalPas()
        return self.acl_users

    security.declareProtected(ViewSurveyResults, 'setCsvHeaders')

    def setCsvHeaders(self, filetype='csv'):
        """Set the CSV headers"""
        REQUEST = self.REQUEST
        file = self.buildSpreadsheetUrl(filetype=filetype)
        REQUEST.RESPONSE.setHeader(
            'Content-Type',
            'text/x-comma-separated-values; charset=utf-8')
        REQUEST.RESPONSE.setHeader(
            'Content-disposition',
            'attachment; filename=%s' % file)
        return REQUEST

    security.declareProtected(ViewSurveyResults, 'buildSpreadsheetUrl')

    def buildSpreadsheetUrl(self, filetype='csv'):
        """Create a filename for the spreadsheets"""
        date = DateTime().strftime("%Y-%m-%d")
        id = self.getId()
        id = "%s-%s" % (id, date)
        url = "%s.%s" % (id, filetype)
        return url

    security.declareProtected(ViewSurveyResults, 'spreadsheet2')

    def spreadsheet2(self):
        """Return spreadsheet 2"""
        self.setCsvHeaders()
        return self.buildSpreadsheet2()

    security.declareProtected(ViewSurveyResults, 'spreadsheet2_tab')

    def spreadsheet2_tab(self):
        """Return spreadsheet 2 tab"""
        self.setCsvHeaders(filetype='tsv')
        dialect = csv.excel_tab
        return self.buildSpreadsheet2(dialect)

    security.declareProtected(ViewSurveyResults, 'buildSpreadsheet2')

    def buildSpreadsheet2(self, dialect=csv.excel):
        """Build spreadsheet 2.
            excel_tab
            excel
        """
        data = StringIO()
        sheet = csv.writer(data, dialect=dialect, quoting=csv.QUOTE_ALL)
        questions = self.getAllQuestionsInOrder()

        sheet.writerow(('user',) + tuple(q.Title()
                       for q in questions) + ('completed',))

        for user in self.getRespondentsList():
            if self.getConfidential():
                row = ['Anonymous']
            else:
                row = [self.getRespondentFullName(user) or user]
            for question in questions:
                answer = question.getAnswerFor(user) or ''
                # handle there being no answer (e.g branched question)
                if answer:
                    if not (isinstance(answer, str) or \
                            isinstance(answer, unicode) or \
                            isinstance(answer, int)):
                        # It's a sequence, filter out empty values
                        answer = ', '.join(filter(None, answer))
                row.append(answer.replace('"', "'").replace('\r\n', ' '))

            row.append(self.checkCompletedFor(user) and
                       'Completed' or 'Not Completed')
            for i, col in enumerate(row):
                if isinstance(col, unicode):
                    col = col.encode('utf8')
                row[i] = col
            sheet.writerow(row)

        return data.getvalue()

    security.declareProtected(ViewSurveyResults, 'spreadsheet3')

    def spreadsheet3(self):
        """Return spreadsheet 3"""
        self.setCsvHeaders()
        return self.buildSpreadsheet3()

    security.declareProtected(ViewSurveyResults,
                              'get_all_questions_in_order_filtered')

    def get_all_questions_in_order_filtered(self,
                                            include_sub_survey=False,
                                            ignore_meta_types=[],
                                            ignore_input_types=[],
                                            restrict_meta_types=[]):
        """This is only used in buildSpreadsheet3, and should be moved into
        another method."""
        questions = self.getAllQuestionsInOrder(
            include_sub_survey=include_sub_survey)
        result = []
        for question in questions:
            ok = True
            if ignore_meta_types:
                if question.meta_type in ignore_meta_types:
                    ok = ok and False
            if ignore_input_types:
                if question.getInputType() in ignore_input_types:
                    ok = ok and False
            if restrict_meta_types:
                if question.meta_type not in restrict_meta_types:
                    ok = ok and False
            if ok:
                result.append(question)
        return result

    security.declareProtected(ViewSurveyResults, 'buildSpreadsheet3')

    def buildSpreadsheet3(self):
        """Build spreadsheet 3."""
        data = StringIO()
        sheet = csv.writer(data)
        questions = self.get_all_questions_in_order_filtered(
            ignore_meta_types=['SurveyMatrix', ])
        sheet.writerow(('user',) + tuple(q.Title()
                       for q in questions) + ('completed',))
        for user in self.getRespondentsList():
            if self.getConfidential():
                row = ['Anonymous']
            else:
                row = [self.getRespondentFullName(user) or user]
            for question in questions:
                answer = ""
                if question.getInputType() in ['text', 'area']:
                    if question.getAnswerFor(user):
                        answer = '"' + question.getAnswerFor(user).replace('"', "'") + '"'
                    else:
                        answer = ""
                elif question.getInputType() in ['checkbox', 'multipleSelect']:
                    options = question.getQuestionOptions()
                    answerList = question.getAnswerFor(user)
                    if answerList and not isinstance(answerList, str):
                        if not isinstance(answerList, list):
                            answerList = [answerList]
                        for option in options:
                            if answerList.count(option) > 0:
                                answer += '1;'
                            else:
                                answer += '0;'
                        answer = '"' + answer[0:len(answer) - 1] + '"'
                    elif answerList:
                        answer = '"' + answerList + '"'
                    else:
                        answer = ''
                else:
                    if not hasattr(question, 'getQuestionOptions'):
                        options = question.title
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
            row.append(self.checkCompletedFor(user) and
                       'Completed' or 'Not Completed')
            sheet.writerow(row)
        return data.getvalue()

    security.declareProtected(ViewSurveyResults, 'summary_spreadsheet')

    def summary_spreadsheet(self):
        """Return summary spreadsheet"""
        self.setCsvHeaders()
        return self.buildSummarySpreadsheet()

    security.declareProtected(permissions.ModifyPortalContent,
                              'buildSummarySpreadsheet')

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
            if question.portal_type in ['Survey Select Question',
                                        'Survey Matrix Question']:
                options = question.getQuestionOptions()
                number_options = question.getAggregateAnswers()
                percentage_options = question.getPercentageAnswers()
                for option in options:
                    row = ['', option]
                    row.append(number_options[option])
                    row.append(percentage_options[option])
                    sheet.writerow(row)
        return data.getvalue()

    security.declareProtected(ViewSurveyResults, 'spreadsheet_select')

    def spreadsheet_select(self):
        """Return spreadsheet select"""
        self.setCsvHeaders()
        try:
            self.REQUEST.form['answers']
        except KeyError:
            return self.buildSelectSpreadsheet()
        return self.buildSelectSpreadsheet(boolean=True)

    security.declareProtected(ViewSurveyResults, 'buildSelectSpreadsheet')

    def buildSelectSpreadsheet(self, boolean=False):
        """Build the select spreadsheet."""
        data = StringIO()
        sheet = csv.writer(data)
        questions = self.getAllSelectQuestionsInOrder()
        row = ['user', ]
        options_row = ['', ]
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
        for user in self.getRespondentsList():
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
                        if type(answer) == int:
                            answer = str(answer)
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
            row.append(self.checkCompletedFor(user) and 'Completed' or
                       'Not Completed')
            sheet.writerow(row)
        return data.getvalue()

    # TODO next two methods are still needed for the tests,
    # but should be removed and the tests fixed
    security.declareProtected(permissions.ModifyPortalContent, 'openFile')

    def openFile(self):
        """open the file, and return the file contents"""
        data_path = os.path.abspath('import')
        try:
            data_catch = open(data_path + '/user_import', 'rU')
        except IOError:  # file does not exist, or path is wrong
            try:
                # we might be in foreground mode
                data_path = os.path.abspath('../import')
                data_catch = open(data_path + '/user_import', 'rU')
            except IOError:  # file does not exist, or path is wrong
                return 'File does not exist'
        input = data_catch.read()
        data_catch.close()
        return input

    security.declareProtected(permissions.ModifyPortalContent,
                              'uploadRespondents')

    def uploadRespondents(self, input=None):
        """upload the respondents"""
        if input is None:
            input = self.openFile()
        input = input.split('\n')
        errors = []
        for user in input:
            if not user:  # empty line
                continue
            user_details = user.split('|')
            if not self.addAuthenticatedRespondent(user_details[1],
                                                   fullname=user_details[0]):
                errors.append(user)
        return errors

    security.declareProtected(permissions.View, 'collective_recaptcha_enabled')

    def collective_recaptcha_enabled(self):
        if using_collective_recaptcha:
            try:
                settings = getRecaptchaSettings()
            except TypeError:
                # collective.recaptcha not configured
                return False
            if settings.public_key and settings.private_key:
                return True
        return False

    security.declareProtected(permissions.ModifyPortalContent, 'pre_validate')

    def pre_validate(self, REQUEST, errors):
        """ checks captcha """
        product_installed = self.portal_quickinstaller.isProductInstalled('quintagroup.plonecaptchas')
        if not product_installed and not self.collective_recaptcha_enabled() and REQUEST.get('showCaptcha', 0):
            if int(REQUEST.get('showCaptcha')):
                errors['showCaptcha'] = _('showCaptcha',
                    default='Product quintagroup.plonecaptchas not installed. '
                            'If you prefer to use the product collective.recaptcha instead of quintagroup.plonecaptchas '
                            'then verifies that recaptcha private and public keys are configured. '
                            'Go to path/to/site/@@recaptcha-settings to configure.')

    security.declareProtected(permissions.View, 'isCaptchaInstalled')

    def isCaptchaInstalled(self):
        """ checks captcha """
        product_installed = self.portal_quickinstaller.isProductInstalled('quintagroup.plonecaptchas')
        return product_installed


    security.declarePrivate('_get_emailInvite_default')

    def _get_emailInvite_default(self):
        foo = _('emailInviteDefault', default=DEFAULT_SURVEY_INVITE)
        translation_service = getToolByName(self, 'translation_service')
        return translation_service.utranslate(domain='plonesurvey',
                                              msgid='emailInviteDefault',
                                              default=DEFAULT_SURVEY_INVITE,
                                              context=self)

registerATCT(Survey, PROJECTNAME)
