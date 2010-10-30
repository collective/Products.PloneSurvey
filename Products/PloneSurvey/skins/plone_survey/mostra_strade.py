## Script (Python) "mostra_strade"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
swt = context.surveywalk_tool

survey_id = context.getSurveyRoot().UID()

utenti = swt.getAllUsers(survey_id)

if utenti <> None:
 for utente in utenti:
  print utente, ':', swt.prettyPrintUserWalk(context.getSurveyRoot().UID(), utente)

return printed


# Esempi:
#
#st.resetStreetForUser('admin') -> cancella la strada di un utente
#print st.doStep('yuri','parte prima') -> fa percorrere un passo all'utente
#st.resetStreet() -> cancella i percorsi di tutti gli utenti
