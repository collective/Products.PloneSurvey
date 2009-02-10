file = context.buildSpreadsheetUrl()
setHeader = context.REQUEST.RESPONSE.setHeader
setHeader('Content-Type','application/vnd.ms-excel')
setHeader('Content-disposition','attachment; filename=%s' % file)

try:
    answers = context.REQUEST.form['answers']
    return context.buildSelectSpreadsheet(boolean=True)
except KeyError:
    return context.buildSelectSpreadsheet()
