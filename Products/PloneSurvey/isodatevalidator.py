from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator
from DateTime import DateTime


class IsoDateValidator:

    __implements__ = IValidator

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        if not value:
            return ("Validation failed(%s): value is "
                    "empty (%s)." % (self.name, repr(value)))
        if not isinstance(value, DateTime):
            if isinstance(value, basestring):
                parts = value.split('-')
                if len(parts) != 3:
                    return ("Validation failed(%s): could not "
                            "convert %s to a ISO format date.""" % (self.name, value))
                if len(parts[1]) > 2:
                    return ("Validation failed(%s): could not "
                            "convert %s to a ISO format date.""" % (self.name, value))
                if len(parts[2]) > 2:
                    return ("Validation failed(%s): could not "
                            "convert %s to a ISO format date.""" % (self.name, value))
                try:
                    parts = [int(x) for x in parts]
                except:
                    return ("Validation failed(%s): could not "
                            "convert %s to a ISO format date.""" % (self.name, value))
                if parts[1] < 1 or parts[1] > 12:
                    return ("Validation failed(%s): could not "
                            "convert %s to a ISO format date.""" % (self.name, value))
                if parts[2] < 1 or parts[2] > 31:
                    return ("Validation failed(%s): could not "
                            "convert %s to a ISO format date.""" % (self.name, value))
                try:
                    value = DateTime(parts[0], parts[1], parts[2])
                except:
                    return ("Validation failed(%s): could not "
                            "convert %s to a ISO format date.""" % (self.name, value))
                return True
            try:
                value = DateTime(value)
            except:
                return ("Validation failed(%s): could not "
                        "convert %s to a ISO format date.""" % (self.name, value))
        return True

validation.register(IsoDateValidator('isValidIsoDate', title='', description=''))
