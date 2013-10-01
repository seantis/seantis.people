from plone.supermodel import loadString, serializeSchema

from seantis.people import tests
from seantis.people.supermodel import (
    get_title_fields,
    set_title_fields,
    get_table_columns,
    set_table_columns
)


class TestSupermodel(tests.IntegrationTestCase):

    xml = """<?xml version='1.0' encoding='utf8'?>
        <model  xmlns="http://namespaces.plone.org/supermodel/schema"
                xmlns:people="http://namespaces.plone.org/supermodel/people">
            <schema>
                <field  name="first"
                        type="zope.schema.TextLine"
                        people:title="true">
                    <description/>
                    <title>Foobar</title>
                </field>
                <field  name="second"
                        type="zope.schema.TextLine"
                        people:title="false"
                        people:column="false">
                    <description/>
                    <title>Foobar</title>
                </field>
                <field  name="third"
                        type="zope.schema.TextLine"
                        people:column="true">
                    <description/>
                    <title>Foobar</title>
                </field>
                <field  name="fourth"
                        type="zope.schema.TextLine"
                        people:title="true">
                    <description/>
                    <title>Foobar</title>
                </field>
            </schema>
        </model>"""

    def test_load_schema(self):
        model = loadString(self.xml)
        self.assertEqual(get_title_fields(model.schema), ['first', 'fourth'])
        self.assertEqual(get_table_columns(model.schema), ['third'])

    def test_write_schema(self):
        model = loadString(self.xml)

        set_title_fields(model.schema, ['second', 'third'])
        set_table_columns(model.schema, ['first'])

        xml = serializeSchema(model.schema)

        # get shorter assertions below
        xml = xml.replace(' type="zope.schema.TextLine"', '')

        self.assertIn('<field name="first" people:column="true">', xml)
        self.assertIn('<field name="second" people:title="true">', xml)
        self.assertIn('<field name="third" people:title="true">', xml)
        self.assertIn('<field name="fourth">', xml)
