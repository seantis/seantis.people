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

class SchemaHandler(object):

    namespace = PEOPLE_NAMESPACE
    prefix = PEOPLE_PREFIX

    def get_attribute_value(self, node, attribute=None, default=''):
        attribute = attribute or self.attribute
        return node.get(ns(attribute, self.namespace), default).lower()


class TitleSchemaHandler(SchemaHandler):

    attribute = 'title'

    def add_title(self, schema, field):
        """ Adds the given field to the schema as a people title field. See
        seantis.people.behaviors.person.NameFromPerson.

        """
        fields = schema.queryTaggedValue(NAME_FROM_PERSON, [])
        fields.append(field)

        set_title_fields(schema, fields)

    def read(self, node, schema, field):
        if self.get_attribute_value(node) == 'true':
            self.add_title(schema, field.__name__)

    def write(self, node, schema, field):
        if field.__name__ in get_title_fields(schema):
            node.set(ns(self.attribute, self.namespace), 'true')


class ColumnSchemaHandler(SchemaHandler):

    attribute = 'column'

    def add_column(self, schema, field, column):
        """ Adds the given field to the schema as a people title field. See
        seantis.people.behaviors.person.NameFromPerson.

        """
        fields = schema.queryTaggedValue(PERSON_COLUMNS, {})
        fields[field] = column

        set_table_columns(schema, fields)

    def read(self, node, schema, field):
        column = self.get_attribute_value(node)
        if column:
            self.add_column(schema, field.__name__, column)

    def write(self, node, schema, field):
        value = get_table_columns(schema).get(field.__name__)
        if value:
            node.set(ns(self.attribute, self.namespace), value)


class PeopleSchema(object):
    """ Handles the people namepsace definitions on the supermodel schema. """

    implements(IFieldMetadataHandler)

    namespace = PEOPLE_NAMESPACE
    prefix = PEOPLE_PREFIX

    handlers = [
        TitleSchemaHandler(),
        ColumnSchemaHandler()
    ]

    def read(self, node, schema, field):
        for handler in self.handlers:
            handler.read(node, schema, field)

    def write(self, node, schema, field):
        for handler in self.handlers:
            handler.write(node, schema, field)


def get_title_fields(schema):
    """ Gets the people-title fields of the schema. """
    return schema.queryTaggedValue(NAME_FROM_PERSON, [])


def set_title_fields(schema, fields):
    """ Sets the people-title fields of the schema. """
    schema.setTaggedValue(NAME_FROM_PERSON, list(set(fields)))


def get_table_columns(schema):
    """ Gets the people-column fields of the schema. """

    return schema.queryTaggedValue(PERSON_COLUMNS, {})


def set_table_columns(schema, fields):
    """ Sets the people-title fields of the schema. The order is defined
    by the field-order, not the order given by the fields-list.

    """
    schema.setTaggedValue(PERSON_COLUMNS, fields)
    
    for column in get_table_columns(schema):
        utils.add_attribute_to_metadata(column)
