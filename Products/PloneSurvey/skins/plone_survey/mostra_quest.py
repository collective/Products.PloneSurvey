## Script (Python) "mostra_quest"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=type='pdf'
##title=
##

#BBB to rename in show_survey o similar, and convert to a browser view
if type <> 'html':
 print '<html>'
 print """<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

<style>
#BBB import the real site name
@import "http://mysite/print.css";
</style> 
</head>"""
else:
 print """<style>
@import "http://mysite/print_web.css";
</style> 
</head>"""


if type <> 'html':
 print '<body>'

print context.getPrint_header().decode("utf-8")

for i in context.objectIds():
 survey = context[i]
 iden = survey.getId()
 if iden not in ['acl_users','riepilogo']:

  questions = quest.getQuestions
  print survey.print_page(questions=questions, quest = survey)

if type <> 'html':
 print '</body>'
 print '</html>'

if type == 'html':
 return context.print_page_html(testo = printed)
else:
 # need an external method called html2pdf which sends the html to an html2pdf util)
 return context.html2pdf(html=printed)
