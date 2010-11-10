## Script (Python) "mostra_quest"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=print_type='pdf'
##title=
##

#BBB to rename in show_survey o similar, and convert to a browser view

def compose(text, phrase):
    return text + phrase

result = ''

if print_type <> 'html':
 compose(result,'<html>')
 compose(result,"""<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

<style>
#BBB import the real site name
@import "http://mysite/print.css";
</style> 
</head>""")
else:
 compose(result,"""<style>
@import "http://mysite/print_web.css";
</style> 
</head>""")
if print_type <> 'html':
 compose(result,'<body>')

compose(result,context.getPrint_header().decode("utf-8"))

for i in context.objectIds():
 survey = context[i]
 iden = survey.getId()
 if iden not in ['acl_users','summary']:
  questions = survey.getQuestions
  compose(result,survey.print_page(questions=questions, quest=survey))

if print_type <> 'html':
 compose(result,'</body>')
 compose(result,'</html>')

if print_type == 'html':
 return context.print_page_html(testo = result)
else:
 # need an external method called html2pdf which sends the html to an html2pdf util)
 return context.html2pdf(html=result)
