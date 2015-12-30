from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.permissions import View
from Products.validation import validation

from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.config import TEXT_VALIDATORS
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion
from Products.PloneSurvey.interfaces.survey_question \
    import IPloneSurveyQuestion
from Products.PloneSurvey.interfaces.survey_text_question \
    import ISurveyTextQuestion
from zope.interface import implements

from schemata import SurveyTextQuestionSchema


class SurveyTextQuestion(BaseQuestion):
    """A textual question within a survey"""
    schema = SurveyTextQuestionSchema
    portal_type = 'Survey Text Question'
    _at_rename_after_creation = True
    security = ClassSecurityInfo()

    implements(IPloneSurveyQuestion, ISurveyTextQuestion)

    @security.protected(View)
    def validateAnswer(self, value, state):
        """Validate the question"""
        if len(value) > self.getMaxLength():

            answertoolong = self.translate(
                default='Answer too long, must have less characters than: ',
                msgid='answer-too-long',
                domain='plonesurvey')

            state.setError(self.getId(), answertoolong +
                           str(self.getMaxLength()))
        else:
            self.addAnswer(value)

    @security.protected(View)
    def getValidators(self):
        """Return a list of validators"""
        validator_list = ['None', ]
        validator_list.extend(TEXT_VALIDATORS)
        return validator_list

    @security.protected(View)
    def validateQuestion(self, value):
        """Return a list of validators"""
        validator = self.getValidation()
        v = validation.validatorFor(validator)
        return v(value)

registerATCT(SurveyTextQuestion, PROJECTNAME)
