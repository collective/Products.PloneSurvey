from Products.Five import BrowserView
from csv import reader, excel
from Products.PloneSurvey import PloneSurveyMessageFactory as _


class importerRespondentsView(BrowserView):
    """
        Browserview for importing respondents from source CSV file
        Dialect is based default Excel export settings (comma)
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.message = ""
        source = self.request.form.get('frm_csv', None)

        if not source:
            self.message = _("No source file given")
            return self.index()

        oExcel = excel()
        oExcel.delimiter = ','
        result = [x for x in reader(source, dialect=oExcel)]

        for x in result:
            if len(x) != 2:
                continue
            fullname = x[0]
            email = x[1]
            self.context.addAuthenticatedRespondent(email,
                                                    fullname=fullname)

        self.message = _("Done importing respondents")

        return self.index()
