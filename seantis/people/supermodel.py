from plone.supermodel.parser import IFieldMetadataHandler
from plone.supermodel.utils import ns

from zope.interface import implements
from zope.schema import getFields

from seantis.people.interfaces import (
    NAME_FROM_PERSON,
    PEOPLE_NAMESPACE,
    PEOPLE_PREFIX
)


class PeopleSchema(object):
    """ Handles the people namepsace definitions on the supermodel schema. """

    implements(IFieldMetadataHandler)

    namespace = PEOPLE_NAMESPACE
    prefix = PEOPLE_PREFIX

    def _add_title(self, schema, field):
        """ Adds the given field to the schema as a people title field. See
        seantis.people.behaviors.person.NameFromPerson.

        """
        fields = schema.queryTaggedValue(NAME_FROM_PERSON, [])
        fields.append(field)

        unique = list(set(fields))
        schema.setTaggedValue(NAME_FROM_PERSON, unique)

    def read(self, fieldNode, schema, field):
        node_value = fieldNode.get(ns('title', self.namespace), 'false')
        if node_value.lower() == 'true':
            self._add_title(schema, field.__name__)

    def write(self, fieldNode, schema, field):
        if field.__name__ in get_title_fields(schema):
            fieldNode.set(ns('title', self.namespace), 'true')


def get_title_fields(schema):
    """ Gets the people-title fields of the schema in order of appearance. """

    order = dict((key, f.order) for key, f in getFields(schema).items())

    return sorted(
        schema.queryTaggedValue(NAME_FROM_PERSON, []), key=order.get
    )


def set_title_fields(schema, fields):
    """ Sets the people-title fields of the schema. The order is defined
    by the field-order, not the order given by the fields-list.

    """

    schema.setTaggedValue(NAME_FROM_PERSON, list(set(fields)))
