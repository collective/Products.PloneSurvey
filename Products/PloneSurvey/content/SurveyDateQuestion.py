from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore import permissions

from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.interfaces.survey_question \
    import IPloneSurveyQuestion

from BaseQuestion import BaseQuestion
from schemata import SurveyDateQuestionSchema


class SurveyDateQuestion(BaseQuestion):
    """A question for date/time within a survey"""
    schema = SurveyDateQuestionSchema
    portal_type = 'Survey Date Question'
    _at_rename_after_creation = True

    implements(IPloneSurveyQuestion)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.ModifyPortalContent, 'post_validate')

    def post_validate(self, REQUEST=None, errors=None):
        """Do the complex validation for the edit form"""
        form = REQUEST.form
        if errors is None:
            errors = {}
        showYMD = form.get('showYMD', None)
        showHM = form.get('showHM', None)
        # Booleans seems not to return 1 or 0, but python True/False
        is_showYMD_set = (showYMD == True)
        is_showHM_set = (showHM == True)
        if not is_showYMD_set and not is_showHM_set:
            errors['showYMD'] = u'At least one of these must be selected.'
            errors['showHM'] = u'At least one of these must be selected.'
            return errors
        elif not is_showYMD_set:
            return errors
        startingYear = form.get('startingYear', None)
        try:
            startingYear = int(startingYear)
        except (TypeError, ValueError):
            # int() raises TypeError, not ValueError or we have to put both
            errors['startingYear'] = u'Start year must be an integer.'
        endingYear = form.get('endingYear', None)
        futureYears = form.get('futureYears', None)
        if endingYear is None and futureYears is None:
            errors['endingYear'] = \
                u'Either end year or future years must be entered.'
            errors['futureYears'] = \
                u'Either end year or future years must be entered.'
            return errors
        elif endingYear and futureYears:
            errors['endingYear'] = \
                u'Both end year and future years can not be entered.'
            errors['futureYears'] = \
                u'Both end year and future years can not be entered.'
            return errors
        if endingYear:
            try:
                endingYear = int(endingYear)
            except ValueError:
                errors['endingYear'] = u'End year must be an integer.'
            if int(startingYear) > int(endingYear):
                errors['endingYear'] = \
                    u'End year can not be before start year.'
        if futureYears:
            try:
                futureYears = int(futureYears)
            except ValueError:
                errors['futureYears'] = u'Future years must be an integer.'
        return errors

    security.declareProtected(permissions.View, 'getInputType')

    def getInputType(self):
        """Return a hard coded input type"""
        return 'date'

    security.declareProtected(permissions.View, 'validateAnswer')

    def validateAnswer(self, form, question_id, state):
        """Validate the question"""
        """Construct the deadline from the form"""
        year = form.get(question_id + '_year', '0')
        month = form.get(question_id + '_month', '0')
        day = form.get(question_id + '_day', '0')
        hour = form.get(question_id + '_hour', '0')
        minute = form.get(question_id + '_minute', '00')
        minute = form.get(question_id + '_minute', '00')
        # TODO this is not going to work outside GMT
        # XXX could do with some validation as well
        value = year + '/' + month + '/' + day + ' ' + hour + \
            ':' + minute + ':00 GMT'
        self.addAnswer(value)

registerATCT(SurveyDateQuestion, PROJECTNAME)
