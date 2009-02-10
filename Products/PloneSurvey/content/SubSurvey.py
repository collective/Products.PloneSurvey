import string
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import PROJECTNAME

from schemata import SubSurveySchema

class SubSurvey(ATCTOrderedFolder):
    """A sub page within a survey"""
    schema = SubSurveySchema
    _at_rename_after_creation = True
    portal_type = 'Sub Survey'
    security = ClassSecurityInfo()

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
        return True

    security.declareProtected(permissions.View, 'getSurveyId')
    def getSurveyId(self):
        """Return the userid for the survey"""
        request = self.REQUEST
        try:
            user_id = request.form['survey_user_id']
        except KeyError:
            pass
        else:
            portal_membership = getToolByName(self, 'portal_membership')
            if not portal_membership.isAnonymousUser():
                if portal_membership.getAuthenticatedMember().getId() == user_id:
                    return user_id
            else:
                survey_cookie = self.aq_parent.getId()
                if self.aq_parent.getAllowAnonymous() and self.REQUEST.has_key(survey_cookie) and request.get(survey_cookie, "Anonymous") == user_id:
                    return user_id
            # XXX survey is probably being spoofed, need another field for allow users without cookies, for now let them through
            return user_id
        survey_url = self.aq_parent.absolute_url()
        return self.REQUEST.RESPONSE.redirect(survey_url)

    security.declareProtected(permissions.ModifyPortalContent, 'getValidationQuestions')
    def getValidationQuestions(self):
        """Return the questions for the validation field"""
        portal_catalog = getToolByName(self, 'portal_catalog')
        questions = [('', 'None')]
        path = string.join(self.aq_parent.getPhysicalPath(), '/')
        results = portal_catalog.searchResults(portal_type = ['Survey Select Question',],
                                               path = path)
        for result in results:
            object = result.getObject()
            questions.append((object.getId(), object.Title() + ', ' + str(object.getQuestionOptions())))
        vocab_list = DisplayList((questions))
        return questions

    security.declareProtected(permissions.View, 'getBranchingCondition')
    def getBranchingCondition(self):
        """Return the title of the branching question"""
        branchings = ''
        required_question = self.getRequiredQuestion()
        branch_question = self[required_question]
        branchings = branch_question.Title()+':'+self.getRequiredAnswer()
        return branchings

    security.declareProtected(permissions.View, 'getQuestions')
    def getQuestions(self):
        """Return the questions for this part of the survey"""
        questions = self.getFolderContents(
            contentFilter={'portal_type':[
                'Survey Matrix',
                'Survey Select Question',
                'Survey Text Question',
                'Survey Two Dimensional',
                ]}, full_objects=True)
        return questions

    security.declareProtected(permissions.View, 'checkCompleted')
    def checkCompleted(self):
        """Return true if this page is completed"""
        # XXX
        return True

    security.declareProtected(permissions.View, 'getNextPage')
    def getNextPage(self):
        """Return the next page of the survey"""
        parent = self.aq_parent
        userid = self.getSurveyId()
        pages = parent.getFolderContents(contentFilter={'portal_type':'Sub Survey',}, full_objects=True)
        num_pages = len(pages)
        for i in range(num_pages):
            if pages[i].getId() == self.getId():
                current_page = i
        while 1==1:
            try:
                next_page = pages[current_page+1]
            except IndexError:
                # no next page, so survey finished
                return parent.exitSurvey()
            if next_page.getRequiredQuestion():
                if not self.getRequiredQuestion():
                    question = self[next_page.getRequiredQuestion()]
                    if next_page.getRequiredAnswerYesNo():
                        if question.getAnswerFor(userid) == next_page.getRequiredAnswer():
                            return next_page()
                    else:
                        if question.getAnswerFor(userid) != next_page.getRequiredAnswer():
                            return next_page()
                else:
                    if self.getRequiredQuestion() != next_page.getRequiredQuestion():
                        try:
                            question = self[next_page.getRequiredQuestion()]
                        except KeyError:
                            next_page = pages[current_page+2]
                            return next_page()
                        if next_page.getRequiredAnswerYesNo():
                            if question.getAnswerFor(userid) == next_page.getRequiredAnswer():
                                return next_page()
                        else:
                            if question.getAnswerFor(userid) != next_page.getRequiredAnswer():
                                return next_page()
            else:
                return next_page()
            current_page += 1

registerATCT(SubSurvey, PROJECTNAME)
