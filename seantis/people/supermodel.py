from plone.supermodel.parser import IFieldMetadataHandler
from plone.supermodel.utils import ns

from zope.interface import implements

from seantis.people import utils
from seantis.people.interfaces import (
    NAME_FROM_PERSON,
    PERSON_COLUMNS,
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

        set_title_fields(schema, fields)

    def _add_table_column(self, schema, field):
        """ Marks the given field as visible in the table view of the people
        directory folder. The field is automatically added to the metadata
        in this case, for performance reasons. 

        """
        fields = schema.queryTaggedValue(PERSON_COLUMNS, [])
        fields.append(field)

        set_table_columns(schema, fields)

    def get_attribute_value(self, node, attribute, default=''):
        return node.get(ns(attribute, self.namespace), default).lower()

    def read(self, fieldNode, schema, field):
        triggers = [
            ('title', 'true', self._add_title),
            ('column', 'true', self._add_table_column)
        ]
        for attribute, expected, handler in triggers:
            if self.get_attribute_value(fieldNode, attribute) == expected:
                handler(schema, field.__name__)

    def write(self, fieldNode, schema, field):
        if field.__name__ in get_title_fields(schema):
            fieldNode.set(ns('title', self.namespace), 'true')
        if field.__name__ in get_table_columns(schema):
            fieldNode.set(ns('column', self.namespace), 'true')


def get_title_fields(schema):
    """ Gets the people-title fields of the schema in order of appearance. """
    return utils.order_fields_by_schema_appearance(
        schema.queryTaggedValue(NAME_FROM_PERSON, []), schema
    )


def set_title_fields(schema, fields):
    """ Sets the people-title fields of the schema. The order is defined
    by the field-order, not the order given by the fields-list.

    """

    schema.setTaggedValue(NAME_FROM_PERSON, list(set(fields)))


def get_table_columns(schema):
    """ Gets the people-column fields of the schema in order of appearance. """

    return utils.order_fields_by_schema_appearance(
        schema.queryTaggedValue(PERSON_COLUMNS, []), schema
    )


def set_table_columns(schema, fields):
    """ Sets the people-title fields of the schema. The order is defined
    by the field-order, not the order given by the fields-list.

    """
    schema.setTaggedValue(PERSON_COLUMNS, list(set(fields)))
    
    for column in get_table_columns(schema):
        utils.add_attribute_to_metadata(column)
