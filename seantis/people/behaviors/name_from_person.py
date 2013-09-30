from plone.app.content.interfaces import INameFromTitle
from zope.interface import implements
from zope.component import adapts

from seantis.people import utils
from seantis.people.supermodel import get_title_fields
from seantis.people.interfaces import INameFromPerson


class NameFromPerson(object):
    """ Uses the fields defined as title by seantis.people.supermodel to
    generate a title for a new object. 

    """
    implements(INameFromTitle)
    adapts(INameFromPerson)

    def __init__(self, context):
        pass

    def __new__(cls, context):
        schema = utils.get_schema_from_portal_type(context.portal_type)

        title = ' '.join([
            getattr(context, field) for field in get_title_fields(schema)
        ])

        instance = super(NameFromPerson, cls).__new__(cls)

        instance.title = title
        context.setTitle(title)

        return instance
