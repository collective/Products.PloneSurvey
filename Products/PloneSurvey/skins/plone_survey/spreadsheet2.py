file = context.buildSpreadsheetUrl()
setHeader = context.REQUEST.RESPONSE.setHeader
setHeader('Content-Type','text/comma-separated-values')
setHeader('Content-disposition','attachment; filename=%s' % file)

return context.buildSpreadsheet2()

