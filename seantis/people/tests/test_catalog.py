from plone import api
from seantis.people import tests
from seantis.people.interfaces import IPerson
from seantis.people.supermodel import set_columns
from seantis.people.supermodel.indexing import on_type_modified


class TestCatalog(tests.IntegrationTestCase):

    def test_require_baseclass(self):
        without_baseclass = self.new_temporary_type(
            behaviors=[IPerson.__identifier__],
        )
        with_baseclass = self.new_temporary_type(
            behaviors=[IPerson.__identifier__],
            klass='seantis.people.types.base.PersonBase'
        )

        on_type_modified(without_baseclass)
        on_type_modified(with_baseclass)

        # create one object with the correct baseclass, one without.
        # both are going to be in portal_catalog, but the one with the
        # person baseclass will end up in the people catalog only.
        with self.user('admin'):
            container = self.new_temporary_folder()
            api.content.create(
                id='without-baseclass',
                type=without_baseclass.id,
                container=container
            )
            api.content.create(
                id='with-baseclass',
                type=with_baseclass.id,
                container=container
            )

        path = '/'.join(container.getPhysicalPath())
        portal_catalog = api.portal.get_tool('portal_catalog')
        people_catalog = api.portal.get_tool('seantis_people_catalog')

        self.assertEqual(
            [b.id for b in portal_catalog(path={'query': path, 'depth': 1})],
            ['without-baseclass', 'with-baseclass']
        )

        self.assertEqual(
            [b.id for b in people_catalog(path={'query': path, 'depth': 1})],
            ['with-baseclass']
        )

    def test_column_metadata(self):
        new_type = self.new_temporary_type(
            behaviors=[IPerson.__identifier__],
            klass='seantis.people.types.base.PersonBase'
        )

        set_columns(new_type.lookupSchema(), [['foo']])
        on_type_modified(new_type)

        with self.user('admin'):
            api.content.create(
                id='123',
                type=new_type.id,
                container=self.new_temporary_folder(),
                foo='bar',
            )

        portal_catalog = api.portal.get_tool('portal_catalog')
        people_catalog = api.portal.get_tool('seantis_people_catalog')

        with self.assertRaises(AttributeError):
            portal_catalog(portal_type=new_type.id)[0].foo

        self.assertEqual(people_catalog(portal_type=new_type.id)[0].foo, 'bar')
