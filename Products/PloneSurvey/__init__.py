from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore.utils import ContentInit
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.permissions import AddPortalContent

# Import "PloneSurveyMessageFactory as _" to create messages
# in plonesurvey domain
from zope.i18nmessageid import MessageFactory
PloneSurveyMessageFactory = MessageFactory('plonesurvey')

from config import SKINS_DIR, GLOBALS, PROJECTNAME
from permissions import addSurvey

registerDirectory(SKINS_DIR, GLOBALS)


def initialize(context):
    import Products.PloneSurvey.content

    ADD_CONTENT_PERMISSIONS = {}
    types = listTypes(PROJECTNAME)
    for aType in types:
        if aType['portal_type'] in ['Survey', ]:
            ADD_CONTENT_PERMISSIONS[aType['portal_type']] = addSurvey
        else:
            ADD_CONTENT_PERMISSIONS[aType['portal_type']] = AddPortalContent

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    allTypes = zip(content_types, constructors)
    for aType, constructor in allTypes:
        kind = "%s: %s" % (PROJECTNAME, aType.portal_type)
        ContentInit(
            kind,
            content_types=(aType,),
            permission=ADD_CONTENT_PERMISSIONS[aType.portal_type],
            extra_constructors=(constructor,),
            fti=ftis,
            ).initialize(context)
