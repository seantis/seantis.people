from textwrap import dedent

from zope import schema

from seantis.people import tests
from seantis.people import interfaces
from seantis.people.errors import PeopleImportError
from seantis.people.content.import_content import (
    get_dataset,
    get_attribute_map,
    get_attribute_values,
    import_people
)


class TestImportContent(tests.IntegrationTestCase):

    def test_import_people_csv(self):
        folder = self.new_temporary_folder()
        model = """<?xml version='1.0' encoding='utf8'?>
        <model  xmlns="http://namespaces.plone.org/supermodel/schema"
                xmlns:people="http://namespaces.plone.org/supermodel/people">
            <schema>
                <field name="firstname" type="zope.schema.TextLine"
                people:title="true">
                    <title>First Name</title>
                </field>
                <field name="lastname" type="zope.schema.TextLine">
                    <title>Last Name</title>
                </field>
            </schema>
        </model>"""

        portal_type = self.new_temporary_type(
            model_source=model,
            behaviors=[interfaces.INameFromPerson.__identifier__],
        ).id

        with self.user('admin'):
            import_people(folder, portal_type, 'csv', dedent("""
                First Name,Last Name,Town
                Peter,Griffin,Quahog
                Glenn,Quagmire,Quahog
            """.lstrip('\n')))

        self.assertEqual(folder['peter'].firstname, 'Peter')
        self.assertEqual(folder['peter'].lastname, 'Griffin')
        self.assertEqual(folder['glenn'].firstname, 'Glenn')
        self.assertEqual(folder['glenn'].lastname, 'Quagmire')

        # no town in the schema
        self.assertFalse(hasattr(folder['peter'], 'town'))
        self.assertFalse(hasattr(folder['glenn'], 'town'))

    def test_get_attribute_values(self):
        casts = [
            (schema.Text, u'Test', u'Test'),
            (schema.Int, u'1', 1),
            (schema.Bool, u'True', True),
            (schema.Bool, u'False', False),
            (schema.Bool, u'True', True),
            (schema.Bool, u'', False)
        ]
        for ix, (fieldtype, value, expected) in enumerate(casts):
            key = str(ix)

            record = {key: value}
            attrmap = {key: fieldtype(__name__=key)}

            result = get_attribute_values(record, attrmap)
            self.assertEqual(result[key], expected)

    def test_get_attribute_values_validation_error(self):
        record = {'test': u'www.example.com'}
        attrmap = {'test': schema.URI(__name__='test')}

        try:
            get_attribute_values(record, attrmap)
        except PeopleImportError, e:
            self.assertEqual(e.colname, 'test')
            self.assertEqual(e.message, u'The specified URI is not valid.')
        else:
            assert False, "The exception should have occured."

    def test_get_csv_dataset(self):
        ds = get_dataset('csv', dedent("""
            First Name,Last Name,Town
            Peter,Griffin,Quahog
            Glenn,Quagmire,Quahog
        """.lstrip('\n')))

        self.assertEqual(ds.headers, ['First Name', 'Last Name', 'Town'])
        self.assertEqual(ds.dict[0], {
            'First Name': 'Peter',
            'Last Name': 'Griffin',
            'Town': 'Quahog'
        })
        self.assertEqual(ds.dict[1], {
            'First Name': 'Glenn',
            'Last Name': 'Quagmire',
            'Town': 'Quahog'
        })

    def test_get_attribute_map(self):
        model = """<?xml version='1.0' encoding='utf8'?>
        <model  xmlns="http://namespaces.plone.org/supermodel/schema">
            <schema>
                <field name="firstname" type="zope.schema.TextLine">
                    <title>First Name</title>
                </field>
                <field name="lastname" type="zope.schema.TextLine">
                    <title>Last Name</title>
                </field>
            </schema>
        </model>"""

        portal_type = self.new_temporary_type(model_source=model).id

        self.assertRaises(
            PeopleImportError, get_attribute_map, [], portal_type
        )

        try:
            get_attribute_map(['firstname', 'First Name'], portal_type)
        except PeopleImportError, e:
            self.assertIn('column is specified more than once', e.message)
        else:
            assert False, "The exception should have occured."

        attrmap = get_attribute_map(['firstname', 'lastname'], portal_type)

        self.assertEqual(len(attrmap), 2)
        self.assertEqual(attrmap['firstname'].__name__, 'firstname')
        self.assertEqual(attrmap['lastname'].__name__, 'lastname')

        attrmap = get_attribute_map(['First Name', 'Last Name'], portal_type)

        self.assertEqual(len(attrmap), 2)
        self.assertEqual(attrmap['First Name'].__name__, 'firstname')
        self.assertEqual(attrmap['Last Name'].__name__, 'lastname')

        attrmap = get_attribute_map(['foo', 'bar'], portal_type)
        self.assertEqual(len(attrmap), 0)
