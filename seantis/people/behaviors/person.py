from zope.interface import implements
from seantis.people.interfaces import IPerson

class Person(object):
    implements(IPerson)

    def __init__(self, context):
        self.context = context
