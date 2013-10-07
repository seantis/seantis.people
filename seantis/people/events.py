from zope.interface import implements
from seantis.people.interfaces import IPeopleSchemaParsedEvent


class PeopleSchemaParsedEvent(object):
    implements(IPeopleSchemaParsedEvent)

    def __init__(self, schema):
        self.schema = schema
