from plone.supermodel.parser import IFieldMetadataHandler
from plone.supermodel.utils import ns

from zope.interface import implements

from seantis.plonetools import utils

NAME_FROM_PERSON = u'seantis.people.name_from_person'
PERSON_COLUMNS = u'seantis.people.person_column'
PERSON_ORDER = u'seantis.people.order'

# Supermodel namespace and prefix
PEOPLE_NAMESPACE = 'http://namespaces.plone.org/supermodel/people'
PEOPLE_PREFIX = 'people'


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


class OrderSchemaHandler(SchemaHandler):

    attribute = 'order'

    def add_order(self, schema, field, index):
        """ Adds the given field to the schema as a people title field. See
        seantis.people.behaviors.person.NameFromPerson.

        """
        order = schema.queryTaggedValue(PERSON_ORDER, {})
        order[field] = index

        set_table_order(schema, order)

    def read(self, node, schema, field):
        index = self.get_attribute_value(node)
        if index:
            self.add_order(schema, field.__name__, index)

    def write(self, node, schema, field):
        value = get_table_order(schema).get(field.__name__)
        if value:
            node.set(ns(self.attribute, self.namespace), value)


class PeopleSchema(object):
    """ Handles the people namepsace definitions on the supermodel schema. """

    implements(IFieldMetadataHandler)

    namespace = PEOPLE_NAMESPACE
    prefix = PEOPLE_PREFIX

    handlers = [
        TitleSchemaHandler(),
        ColumnSchemaHandler(),
        OrderSchemaHandler()
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


def get_table_columns_merged(schema):
    """ Returns the columns in the order of appearance in the table with
    each column having a tuple with a list of titles and a corresponding
    list of attributes.

    """
    columns = utils.invert_dictionary(get_table_columns(schema))

    for index in sorted(columns):
        attributes = utils.order_fields_by_schema(
            columns[index], schema
        )

        titles = [schema[attr].title for attr in attributes]

        yield (titles, attributes)


def get_table_order(schema):
    """ Gets the fields which are used as sort order in the table. """
    return schema.queryTaggedValue(PERSON_ORDER, {})


def set_table_order(schema, order):
    """ Sets the fields used as sort order on the table. """
    schema.setTaggedValue(PERSON_ORDER, order)


def get_table_order_flat(schema):
    """ Generates a sorted list out of the raw dictionary of the schema. """
    order = utils.invert_dictionary(get_table_order(schema))

    for index in sorted(order):
        for item in order[index]:
            yield item

def set_table_order_flat(schema, fields):
    """ Stores the given list in the raw dictionary format of the schema. """
    order = dict((field, str(ix+1)) for ix, field in enumerate(fields))
    set_table_order(schema, order)
