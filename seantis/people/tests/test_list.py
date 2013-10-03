from plone import api

from seantis.people.interfaces import IPerson
from seantis.people.content import List
from seantis.people import tests


class TestList(tests.IntegrationTestCase):

    def test_list_creation(self):
        with self.user('admin'):
            lst = api.content.create(
                id='test',
                type='seantis.people.list',
                container=self.new_temporary_folder()
            )

        self.assertIs(type(lst.aq_base), List)

    def test_list_people_by_behavior(self):
        with self.user('admin'):
            lst = api.content.create(
                id='test',
                type='seantis.people.list',
                container=self.new_temporary_folder()
            )

            person = lambda: self.new_temporary_type(
                behaviors=[IPerson.__identifier__]
            )
            beast = lambda: self.new_temporary_type()

            king = person()
            prince = person()
            wolf = beast()

            api.content.create(id='ned', type=king.id, container=lst)
            api.content.create(id='robb', type=prince.id, container=lst)
            api.content.create(id='lady', type=wolf.id, container=lst)

        self.assertEqual(len(lst.people()), 2)  # the wolf doesn't count

    def test_list_view_empty(self):
        with self.user('admin'):
            lst = api.content.create(
                id='test',
                type='seantis.people.list',
                container=self.new_temporary_folder()
            )

            view = lst.unrestrictedTraverse('@@view')
        
        self.assertIn('No people in the list.', view())
