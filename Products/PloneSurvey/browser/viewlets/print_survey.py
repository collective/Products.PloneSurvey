from Products.Five.browser import BrowserView

class PrintSurveyView(BrowserView):
    """A printable view of a survey, rendered as a pdf"""

    def name(self):
        return self.context.Title()
