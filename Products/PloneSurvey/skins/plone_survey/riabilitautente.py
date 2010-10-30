## Script (Python) "riabilitautente"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=userid
##title=
##
completed = context.getCompletedFor()
if userid in completed:
 completed.remove(userid)
 context.setCompletedFor(completed)
 print 'fatto'
else:
 print 'utente non presente'

return printed

