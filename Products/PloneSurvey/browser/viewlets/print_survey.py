# Since Plone4.3 ViewPageTemplateFile moved to zope.browserpage
try:
    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
except:
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from z3c.rml.rml2pdf import parseString
from Products.Five.browser import BrowserView


class PrintSurveyView(BrowserView):
    """A printable view of a survey, rendered as a pdf"""

    def __call__(self):
        self.request.response.setHeader('content-type', 'application/pdf')
        rml_doc = ViewPageTemplateFile('print_survey.pt')(self)
        return parseString(rml_doc.encode('utf-8')).read()

    def name(self):
        return self.context.Title()

    def getAllQuestionsInOrder(self):
        return self.context.getAllQuestionsInOrder(include_sub_survey=True)
