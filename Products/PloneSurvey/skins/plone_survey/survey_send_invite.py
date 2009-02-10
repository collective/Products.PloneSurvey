##parameters=email

from Products.CMFCore.utils import getToolByName
portal_properties   = getToolByName(context, 'portal_properties')
site_props          = portal_properties.site_properties

acl_users = context.get_acl_users()

if email == 'all':
    email = acl_users.getUserNames()
elif not same_type(email, []):
    email = [email]

for eml in email:
    user = acl_users.getUserById(eml)

    mail_text = context.survey_send_invite_template(
        context.REQUEST,
        user=user, 
        recipient=user.getId(),
        subject="Survey %s" % context.title_or_id())  
    
    host = context.MailHost
    mail_text = mail_text.encode(site_props.default_charset or 'utf-8')
    host.send(mail_text)

pu = getToolByName(context, 'plone_utils')
pu.addPortalMessage("Survey invite sent to %s recipients" % len(email))
context.REQUEST.RESPONSE.redirect(context.REQUEST.HTTP_REFERER)
