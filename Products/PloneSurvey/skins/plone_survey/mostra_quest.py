## Script (Python) "mostra_quest"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=tipo='pdf'
##title=
##

if tipo <> 'html':
 print '<html>'
 print """<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

<style>
@import "http://q.cab.unipd.it/print.css";
</style> 
</head>"""
else:
 print """<style>
@import "http://q.cab.unipd.it/print_web.css";
</style> 
</head>"""


if tipo <> 'html':
 print '<body>'

print context.getPrint_header().decode("utf-8")

for i in context.objectIds():
 quest = context[i]
 iden = quest.getId()
 if iden not in ['acl_users','riepilogo']:

  questions = quest.getQuestions
  print quest.print_page(questions=questions, quest = quest)

if tipo <> 'html':
 print '</body>'
 print '</html>'

if tipo == 'html':
 return context.print_page_html(testo = printed)
else:
 return context.html2pdf(html=printed)
