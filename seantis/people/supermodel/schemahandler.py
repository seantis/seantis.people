from collections import namedtuple

from plone.supermodel.parser import IFieldMetadataHandler
from plone.supermodel.utils import ns

from zope.interface import implements

from seantis.plonetools import tools

NAME_FROM_PERSON = u'seantis.people.name_from_person'
PERSON_COLUMNS = u'seantis.people.person_column'
PERSON_ORDER = u'seantis.people.order'
PERSON_SELECTABLE = u'seantis.people.selectable'

# Supermodel namespace and prefix
PEOPLE_NAMESPACE = 'http://namespaces.plone.org/supermodel/people'
PEOPLE_PREFIX = 'people'

missing = object()


def get_title_fields(schema):
    """ Gets the people-title fields of the schema. """
    return schema.queryTaggedValue(NAME_FROM_PERSON, [])


def set_title_fields(schema, fields):
    """ Sets the people-title fields of the schema. """
    schema.setTaggedValue(NAME_FROM_PERSON, list(set(fields)))


def get_selectable_fields(schema):
    """ Gets the selectable fields of the schema. Those are displayed
    on the list view as combo boxes. """
    return schema.queryTaggedValue(PERSON_SELECTABLE, [])


def set_selectable_fields(schema, fields):
    """ Sets the selectable fields of the schema. Those are displayed
    on the list view as combo boxes. """
    schema.setTaggedValue(PERSON_SELECTABLE, list(set(fields)))


def get_table_columns(schema):
    """ Gets the people-column fields of the schema. """

    return schema.queryTaggedValue(PERSON_COLUMNS, {})


def set_table_columns(schema, fields):
    """ Sets the people-title fields of the schema. The order is defined
    by the field-order, not the order given by the fields-list.

    """
    schema.setTaggedValue(PERSON_COLUMNS, fields)

    for column in get_table_columns(schema):
        tools.add_attribute_to_metadata(column)


def get_table_columns_merged(schema):
    """ Returns the columns in the order of appearance in the table with
    each column having a list of titles, a corresponding list of attributes and
    a flag indicating wheter the column contains more than one field.

    """
    Column = namedtuple(
        'Column',
        ['titles', 'attributes', 'single_attribute', 'wrap_in_link']
    )
    columns = tools.invert_dictionary(get_table_columns(schema))
    title_fields = get_title_fields(schema)

    for index in sorted(columns):
        attributes = tools.order_fields_by_schema(
            columns[index], schema
        )

        wrap_in_link = False

        titles = []
        for attribute in attributes:
            titles.append(schema[attribute].title)

            if attribute in title_fields:
                wrap_in_link = True

        titles = [schema[attr].title for attr in attributes]

        yield Column(titles, attributes, len(titles) == 1, wrap_in_link)


def get_table_order_raw(schema):
    """ Gets the fields which are used as sort order in the table. """
    return schema.queryTaggedValue(PERSON_ORDER, {})


def set_table_order_raw(schema, order):
    """ Sets the fields used as sort order on the table. """
    schema.setTaggedValue(PERSON_ORDER, order)


def get_table_order(schema):
    """ Generates a sorted list out of the raw dictionary of the schema. """
    order = tools.invert_dictionary(get_table_order_raw(schema))

    for index in sorted(order):
        for item in order[index]:
            yield item


def set_table_order(schema, fields):
    """ Stores the given list in the raw dictionary format of the schema. """
    order = dict((field, str(ix+1)) for ix, field in enumerate(fields))
    set_table_order_raw(schema, order)


class SchemaHandler(object):

    namespace = PEOPLE_NAMESPACE
    prefix = PEOPLE_PREFIX

    def get_node_value(self, node, default=missing):
        value = node.get(ns(self.attribute, self.namespace), default)
        if isinstance(value, basestring):
            return value.lower()
        else:
            return value

    def set_node_value(self, node, value):
        node.set(ns(self.attribute, self.namespace), value)

    def get_attribute(self, schema, field):
        raise NotImplementedError

    def set_attribute(self, schema, field, value):
        raise NotImplementedError

    def read(self, node, schema, field):
        value = self.get_node_value(node)
        if value is not missing:
            self.set_attribute(schema, field, value)

    def write(self, node, schema, field):
        value = self.get_attribute(schema, field)
        if value is not missing:
            self.set_node_value(node, value)


class FieldListSchemaHandler(SchemaHandler):

    setter, getter = None, None

    def get_attribute(self, schema, field):
        if field.__name__ in self.getter(schema):
            return 'true'
        else:
            return missing

    def set_attribute(self, schema, field, value):
        if value == 'true':
            fields = self.getter(schema)
            fields.append(field.__name__)

            self.setter(schema, fields)


class DictionarySchemaHandler(SchemaHandler):

    setter, getter = None, None

    def get_attribute(self, schema, field):
        return self.getter(schema).get(field.__name__, missing)

    def set_attribute(self, schema, field, value):
        fields = self.getter(schema)
        fields[field.__name__] = value

        self.setter(schema, fields)


class TitleSchemaHandler(FieldListSchemaHandler):

    attribute = 'title'
    getter = staticmethod(get_title_fields)
    setter = staticmethod(set_title_fields)


class ColumnSchemaHandler(DictionarySchemaHandler):

    attribute = 'column'
    getter = staticmethod(get_table_columns)
    setter = staticmethod(set_table_columns)


class OrderSchemaHandler(DictionarySchemaHandler):

    attribute = 'order'
    getter = staticmethod(get_table_order_raw)
    setter = staticmethod(set_table_order_raw)


class SelectableSchemaHandler(FieldListSchemaHandler):

    attribute = 'selectable'
    getter = staticmethod(get_selectable_fields)
    setter = staticmethod(set_selectable_fields)


class PeopleSchema(object):
    """ Handles the people namepsace definitions on the supermodel schema. """

    implements(IFieldMetadataHandler)

    namespace = PEOPLE_NAMESPACE
    prefix = PEOPLE_PREFIX

    handlers = [
        TitleSchemaHandler(),
        ColumnSchemaHandler(),
        OrderSchemaHandler(),
        SelectableSchemaHandler()
    ]

    def read(self, node, schema, field):
        for handler in self.handlers:
            handler.read(node, schema, field)

    def write(self, node, schema, field):
        for handler in self.handlers:
            handler.write(node, schema, field)
