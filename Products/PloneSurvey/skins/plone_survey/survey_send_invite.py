##parameters=email
_ = context.translate

from Products.CMFCore.utils import getToolByName
portal_properties = getToolByName(context, 'portal_properties')

acl_users = context.get_acl_users()
pu = getToolByName(context, 'plone_utils')

if email == 'all':
    invites_sent = context.sendSurveyInviteAll(send_to_all=True)
    pu.addPortalMessage(_("Survey invite sent to ${invites_sent} recipients",
                          domain="plonesurvey",
                          mapping={'invites_sent': invites_sent}))
elif email == 'new':
    invites_sent = context.sendSurveyInviteAll(send_to_all=False)
    pu.addPortalMessage(_("Survey invite sent to ${invites_sent} recipients",
                          domain="plonesurvey",
                          mapping={'invites_sent': invites_sent}))
else:
    context.sendSurveyInvite(email)
    pu.addPortalMessage(_("Survey invite sent to ${email}",
                          domain="plonesurvey",
                          mapping={'email': email}))

context.REQUEST.RESPONSE.redirect(context.REQUEST.HTTP_REFERER)
