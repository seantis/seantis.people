import tablib

from plone import api

from zope.schema import getFields
from zope.schema.interfaces import IFromUnicode, ValidationError

from seantis.people import _
from seantis.people.errors import PeopleImportError
from seantis.plonetools import tools

supported_formats = ('csv', )


def import_people(container, portal_type, format, data):
    dataset = get_dataset(format, data)
    attribute_map = get_attribute_map(dataset.headers, portal_type)

    for ix, record in enumerate(dataset.dict):
        try:
            values = get_attribute_values(record, attribute_map)
            api.content.create(
                container=container,
                type=portal_type,
                id='',
                **values
            )
        except PeopleImportError, e:
            raise PeopleImportError(
                e.message, rownumber=ix+1, colname=e.colname
            )
        except Exception, e:
            raise PeopleImportError(e.message, rownumber=ix+1)


def get_dataset(format, data):
    assert format in supported_formats

    def get_dataset_from_csv():
        ds = tablib.Dataset()
        ds.csv = data

        return ds

    return locals()['get_dataset_from_{}'.format(format)]()


def get_attribute_map(headers, portal_type):

    if not headers:
        raise PeopleImportError(_(u'No column headers were found'))

    schema = tools.get_schema_from_portal_type(portal_type)
    attribute_map = {}

    fields = getFields(schema)

    known_titles = dict((field.title, field) for field in fields.values())
    known_fields = dict((key, field) for key, field in fields.items())

    for header in headers:

        if header in known_fields:
            field = known_fields[header]
        elif header in known_titles:
            field = known_titles[header]
        else:
            continue

        if field in attribute_map.values():
            raise PeopleImportError(
                _(
                    u'The ${name} column is specified more than once',
                    mapping=dict(name=header)
                )
            )

        attribute_map[header] = field

    return attribute_map


def get_attribute_values(record, attribute_map):
    values = {}

    for header, field in attribute_map.items():

        assert IFromUnicode.providedBy(field), """
            {} does not support fromUnicode
        """.format(field)

        try:
            values[field.__name__] = field.fromUnicode(record[header])
        except ValidationError, e:
            raise PeopleImportError(e.doc(), colname=header)
        except ValueError, e:
            raise PeopleImportError(e.message, colname=header)

    return values
