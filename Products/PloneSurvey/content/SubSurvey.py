import string
from AccessControl import ClassSecurityInfo

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.CMFCore.utils import getToolByName

from Products.PloneSurvey import permissions

schema = ATContentTypeSchema.copy() + Schema((

    StringField('requiredQuestion',
        schemata="Branching",
        searchable=0,
        required=0,
        vocabulary='getValidationQuestions',
        widget=SelectionWidget(
            format="radio",
            label="Conditional Question",
            label_msgid="label_previous_question",
            description="""The conditional question determines whether to display this Sub Survey.
            Select 'None' to display the Sub Survey unconditionally.""",
            description_msgid="help_previous_question",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('requiredAnswer',
        schemata="Branching",
        searchable=0,
        required=0,
        vocabulary='getQuestions',
        widget=StringWidget(
            label="Required Answer",
            label_msgid="label_previous_question_answer",
            description="""Enter a required answer to the conditional question above to determine
            whether this Sub Survey is displayed.""",
            description_msgid="help_previous_question_answer",
            i18n_domain="plonesurvey",
          ),
        ),

    BooleanField('requiredAnswerYesNo',
        schemata="Branching",
        searchable=0,
        required=0,
        default=1,
        widget=BooleanWidget(
            label="Use Required Answer?",
            label_msgid="label_previous_question_answer_yes_no",
            description="Check this box if the required answer should be selected for this Sub Survey to be displayed.",
            description_msgid="help_previous_question_answer_yes_no",
            i18n_domain="plonesurvey",
          ),
        ),

    ))

finalizeATCTSchema(schema, moveDiscussion=False)
schema["description"].widget.label = "Survey description"
schema["description"].widget.label_msgid = "label_description"
schema["description"].widget.description = "Add a short description of the survey here."
schema["description"].widget.description_msgid = "help_description"
schema["description"].widget.i18n_domain = "plonesurvey"
del schema["relatedItems"]

class SubSurvey(ATCTOrderedFolder):
    """A sub page within a survey"""
    schema = schema
    _at_rename_after_creation = True

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
                parent.setCompletedForUser()
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

registerType(SubSurvey)
