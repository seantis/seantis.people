import re

from plone.supermodel import loadString, serializeSchema

from seantis.people import tests
from seantis.people.supermodel import (
    get_title_fields,
    set_title_fields,
    get_columns,
    set_columns,
    get_order,
    set_order,
    get_selectable_fields,
    set_selectable_fields,
)


class TestSupermodel(tests.IntegrationTestCase):

    def deprettify(self, xml):
        return re.sub(' +',' ',xml.replace('\n', '')).replace('> <', '><')

    title_xml = """<?xml version='1.0' encoding='utf8'?>
        <model  xmlns="http://namespaces.plone.org/supermodel/schema"
                xmlns:people="http://namespaces.plone.org/supermodel/people">
            <schema>
                <people:title>
                    <people:item>foo</people:item>
                    <people:item>bar</people:item>
                </people:title>
            </schema>
        </model>"""

    def test_load_title_schema(self):
        model = loadString(self.title_xml)
        self.assertEqual(
            get_title_fields(model.schema),
            ['foo', 'bar']
        )

    def test_write_title_schema(self):
        model = loadString(self.title_xml)
        set_title_fields(model.schema, ['stop', 'hammertime'])
        xml = serializeSchema(model.schema)

        self.assertIn('<people:item>stop</people:item>', xml)
        self.assertIn('<people:item>hammertime</people:item>', xml)
        self.assertTrue(
            xml.find('<people:item>stop</people:item>') < 
            xml.find('<people:item>hammertime</people:item>')
        )

    column_xml = """<?xml version='1.0' encoding='utf8'?>
        <model  xmlns="http://namespaces.plone.org/supermodel/schema"
                xmlns:people="http://namespaces.plone.org/supermodel/people">
            <schema>
                <people:columns>
                    <people:column>
                        <people:item>first</people:item>
                        <people:item>second</people:item>
                    </people:column>
                    <people:column>
                        <people:item>fourth</people:item>
                    </people:column>
                </people:columns>
            </schema>
        </model>"""

    def test_load_column_schema(self):
        model = loadString(self.column_xml)
        self.assertEqual(
            get_columns(model.schema), 
            [['first', 'second'], ['fourth']]
        )

    def test_write_column_schema(self):
        model = loadString(self.column_xml)
        set_columns(
            model.schema, [['first'], ['third', 'fourth']]
        )
        xml = self.deprettify(serializeSchema(model.schema))

        self.assertIn('<people:column><people:item>first</people:item>', xml)
        self.assertIn('<people:column><people:item>third</people:item>', xml)
        self.assertIn('</people:item><people:item>fourth</people:item>', xml)

        self.assertTrue(
            xml.find('<people:item>first</people:item>') <
            xml.find('<people:item>third</people:item>') <
            xml.find('<people:item>fourth</people:item>')
        )

    order_xml = """<?xml version='1.0' encoding='utf8'?>
        <model  xmlns="http://namespaces.plone.org/supermodel/schema"
                xmlns:people="http://namespaces.plone.org/supermodel/people">
            <schema>
                <people:order>
                    <people:item>first</people:item>
                    <people:item>second</people:item>
                    <people:item>third</people:item>
                </people:order>
            </schema>
        </model>"""

    def test_load_order_schema(self):
        model = loadString(self.order_xml)
        self.assertEqual(
            list(get_order(model.schema)),
            ['first', 'second', 'third']
        )

    def test_write_order_schema(self):
        model = loadString(self.order_xml)
        set_order(model.schema, ['third', 'second', 'first'])
        xml = serializeSchema(model.schema)

        self.assertIn('<people:item>third</people:item>', xml)
        self.assertIn('<people:item>second</people:item>', xml)
        self.assertIn('<people:item>first</people:item>', xml)
        self.assertTrue(
            xml.find('<people:item>third</people:item>') < 
            xml.find('<people:item>second</people:item>') <
            xml.find('<people:item>first</people:item>')
        )

    selectable_schema = """<?xml version='1.0' encoding='utf8'?>
        <model  xmlns="http://namespaces.plone.org/supermodel/schema"
                xmlns:people="http://namespaces.plone.org/supermodel/people">
            <schema>
                <people:columns>
                    <people:column selectable="true">
                        <people:item>works</people:item>
                    </people:column>
                    <people:column selectable="true">
                        <people:item>does</people:item>
                        <people:item>not</people:item>
                    </people:column>
                    <people:column>
                        <people:item>spare</people:item>
                    </people:column>
                </people:columns>                
            </schema>
        </model>"""

    def test_load_selectable_schema(self):
        model = loadString(self.selectable_schema)

        # only colums with one field may be selectable
        self.assertEqual(
            sorted(get_selectable_fields(model.schema)),
            ['works']
        )

    def test_write_selectable_schema(self):
        model = loadString(self.selectable_schema)
        set_selectable_fields(model.schema, ['spare'])
        xml = self.deprettify(serializeSchema(model.schema))

        self.assertIn(
            '<people:column selectable="true"><people:item>spare', xml
        )
