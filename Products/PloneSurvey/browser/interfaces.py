from zope.interface import Interface


class IPloneSurveySpecific(Interface):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "PloneSurvey" theme, this interface must be its layer
       (in my_theme/viewlets/configure.zcml).
    """
