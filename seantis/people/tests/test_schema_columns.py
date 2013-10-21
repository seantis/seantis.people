from plone.supermodel import loadString

from seantis.people import tests
from seantis.people.supermodel import (
    get_schema_columns,
    set_columns,
    set_title_fields
)


class TestSchemaColumns(tests.IntegrationTestCase):

    address_model = """<?xml version='1.0' encoding='utf8'?>
        <model  xmlns="http://namespaces.plone.org/supermodel/schema"
                xmlns:people="http://namespaces.plone.org/supermodel/people">
            <schema>
                <field  name="lastname" type="zope.schema.TextLine">
                    <title>Nachname</title>
                </field>
                <field  name="firstname" type="zope.schema.TextLine">
                    <title>Vorname</title>
                </field>
                <field  name="town" type="zope.schema.TextLine">
                    <title>Ort</title>
                </field>
                <field  name="country" type="zope.schema.TextLine">
                    <title>Land</title>
                </field>
            </schema>
        </model>"""

    def test_no_columns(self):

        model = loadString(self.address_model)
        columns = get_schema_columns(model.schema)

        self.assertEqual(columns, [])

    def test_one_column(self):

        model = loadString(self.address_model)

        set_columns(model.schema, [['lastname']])
        columns = get_schema_columns(model.schema)

        self.assertEqual(len(columns), 1)
        self.assertEqual(columns[0].schema, model.schema)
        self.assertEqual(columns[0].fields, ['lastname'])
        self.assertEqual(columns[0].titles, [u'Nachname'])
        self.assertEqual(columns[0].contains_title_field, False)

    def test_merged_columns(self):

        model = loadString(self.address_model)

        set_columns(model.schema, [['country', 'lastname']])
        columns = get_schema_columns(model.schema)

        self.assertEqual(len(columns), 1)

        # ordered by field order
        self.assertEqual(columns[0].fields, ['lastname', 'country'])
        self.assertEqual(columns[0].titles, [u'Nachname', u'Land'])
        self.assertEqual(columns[0].contains_title_field, False)

    def test_contains_title_field(self):

        model = loadString(self.address_model)

        set_columns(model.schema, [['country', 'lastname']])

        columns = get_schema_columns(model.schema)
        self.assertEqual(columns[0].contains_title_field, False)

        set_title_fields(model.schema, ['lastname'])
        columns = get_schema_columns(model.schema)
        self.assertEqual(columns[0].contains_title_field, True)

        set_title_fields(model.schema, ['firstname'])
        columns = get_schema_columns(model.schema)
        self.assertEqual(columns[0].contains_title_field, False)

        set_columns(model.schema, [['firstname']])
        columns = get_schema_columns(model.schema)
        self.assertEqual(columns[0].contains_title_field, True)
