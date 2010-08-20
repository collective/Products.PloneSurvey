##parameters=email

from Products.CMFCore.utils import getToolByName
portal_properties   = getToolByName(context, 'portal_properties')

acl_users = context.get_acl_users()
pu = getToolByName(context, 'plone_utils')

if email == 'all':
    invites_sent = context.sendSurveyInviteAll(send_to_all=True)
    pu.addPortalMessage("Survey invite sent to %s recipients" % invites_sent)
elif email == 'new':
    invites_sent = context.sendSurveyInviteAll(send_to_all=False)
    pu.addPortalMessage("Survey invite sent to %s recipients" % invites_sent)
else:
    context.sendSurveyInvite(email)
    pu.addPortalMessage("Survey invite sent to %s" % email)

context.REQUEST.RESPONSE.redirect(context.REQUEST.HTTP_REFERER)
