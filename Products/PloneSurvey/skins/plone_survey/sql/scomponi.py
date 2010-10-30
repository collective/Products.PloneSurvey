## Script (Python) "scomponi"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=carattere='§'
##title=
##
#carattere = '§'


sep = carattere + ',' + carattere
def fai_stringa(vett):
 vett1 = []
 for v in vett:
  vett1.append(v.replace('"','""'))
 return carattere + sep.join(vett1) + carattere

def crea_schema(vett, nome_tabella, nome_database):
 vett1 = []
 string = "DROP DATABASE IF EXISTS " + nome_database + "; CREATE DATABASE " + nome_database + " CHARACTER SET utf8 COLLATE utf8_general_ci; USE " + nome_database + "; "
 string = string + "CREATE TABLE " + nome_tabella + "( " 
 cont = {}
 for v in vett:
  try:
   x = float(v)
   # devo convertire un numero in stringa
   v = 'colonna'+v
  except ValueError:
   pass
  nome = pu.normalizeString(v).replace('-','_')
  if nome + " text" in vett1:
   cont[nome] = cont[nome] + 1
   nome = nome + str(cont[nome])
  else:
   cont[nome] = 1
  vett1.append(nome + " text")
 return string  + ','.join(vett1) + ");\n"

def crea_riga(vett, nome_tabella):
 vett1 = []
 string = "INSERT INTO " + nome_tabella + " VALUES ( " 
 for v in vett:
  vett1.append('"' + v + '"')
 return string  + ' ,'.join(vett1) + ");\n"


pu = context.plone_utils
#today=DateTime()
#now = context.ZopeTime()
survey = context.getSurveyRoot()
nome_db = pu.normalizeString(survey.Title() + "_" + survey.UID()).replace('-','_')
#try:
# context.sql.agg_db(dbid=nome_db)
#except:
# #the database exists
# pass
#return nome_db

sql = ""
if 1 == 1:
        tabella = {}
        questions = context.getAllQuestionsInOrder()
#        domande = [q.Title() for q in questions]
        domande = []
        for q in questions:
         if q.meta_type == "SurveyMatrixQuestion" and q.getInputType() not in ['radio', 'checkbox']:
          for opt in q.getQuestionOptions():
           domande.append(q.getId() + "-" + opt)
         else:
          domande.append(q.Title())
	colonne = ["user"] + domande + ["completed"]
	sql = sql + crea_schema(colonne, "principale", nome_db)
#        print fai_stringa(["user"] + domande + ["completed"])

        for user in context.getRespondents():
            if context.getConfidential():
                row = ['Anonymous']
            else:
                row = [context.getRespondentFullName(user) or user]
            for question in questions:
                answer = question.getAnswerFor(user) or ''
                if question.meta_type == "SurveyMatrixQuestion":
                 lunghezza_campo = len(question.getQuestionOptions())
                 if answer <> None:
                  if (same_type(answer, []) or same_type(answer, ())) and question.getInputType() not in ['radio', 'checkbox']:
                   for i in range(0, lunghezza_campo):
                    try:
                     row.append(str(answer[i].encode("utf-8")))
                    except:
                     row.append('')
                  else:
                     row.append(str(answer))
                 else:
                  for opt in question.getQuestionOptions():
                    row.append('Non prevista')
                else:
                 if question.meta_type == "SurveyGridQuestion":
                  if question.getId() + ' - ' + question.Title() not in tabella.keys():
                   tabella[question.getId() + ' - ' + question.Title()] = []
                  columns = question.getAllColumns()
                  for i in answer:
                    linea = [ (context.getRespondentFullName(user) or user) ]
                    for column in columns:
                      linea.append(i[column])
                    tabella[question.getId() + ' - ' + question.Title()].append(fai_stringa(linea))
                  row.append('')
                 else:
		  if question.meta_type == "SurveySelectQuestion":
		   if same_type(answer, ''):
		    row.append(str(answer))
		   else:
		    # ho una lista o una tupla
                    row.append(', '.join(answer))
		  else:
		   row.append(str(answer))

            row.append(context.checkCompletedFor(user) and 'Completed' or 'Not Completed')
            sql = sql + crea_riga(row, "principale")

        return sql
        for k in tabella.keys():
         print carattere + k + carattere
         for t in tabella[k]:
          print t

        return printed

