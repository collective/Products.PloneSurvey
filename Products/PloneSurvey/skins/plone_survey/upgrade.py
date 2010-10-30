## Script (Python) "upgrade"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
uid =  context.UID()


st = context.surveywalk_tool
st.registerSurvey(uid)

return 'upgrade fatto'

#st.resetWalkForUser(survey='test-stampa-questionario',userid='admin')

# Esempi:
#
#st.resetStreetForUser('admin') -> cancella la strada di un utente
#print st.doStep('yuri','parte prima') -> fa percorrere un passo all'utente
#st.resetStreet() -> cancella i percorsi di tutti gli utenti

