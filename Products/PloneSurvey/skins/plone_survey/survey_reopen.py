## Script (Python) "survey_send_invite"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=email
##title=
##

from Products.CMFCore.utils import getToolByName
completed = context.getCompletedFor()
if email in completed:
 completed.remove(email)
context.setCompletedFor(completed)

pu = getToolByName(context, 'plone_utils')
pu.addPortalMessage("Questionario riaperto per l'utente %s" % email)
context.REQUEST.RESPONSE.redirect(context.REQUEST.HTTP_REFERER)

