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

            new_person_type = lambda: self.new_temporary_type(
                behaviors=[IPerson.__identifier__]
            )

            person = new_person_type()
            new_person_type()  # intentionally unused

            # all types are possible before any are used
            self.assertEqual(len(lst.possible_types()), 2)
            self.assertEqual(len(lst.available_types()), 2)
            self.assertEqual(lst.used_type(), None)

            api.content.create(id='ned', type=person.id, container=lst)
            api.content.create(id='robb', type=person.id, container=lst)

            # only one type is used at this point
            self.assertEqual(len(lst.people()), 2)
            self.assertEqual(len(lst.possible_types()), 2)
            self.assertEqual(len(lst.available_types()), 1)
            self.assertEqual(lst.used_type(), person)

    def test_add_unsupported_type(self):
        with self.user('admin'):
            lst = api.content.create(
                id='test',
                type='seantis.people.list',
                container=self.new_temporary_folder()
            )

            add_invalid_type = lambda: api.content.create(
                id='invalid', type=self.new_temporary_type(), container=lst
            )

        self.assertRaises(api.exc.InvalidParameterError, add_invalid_type)

    def test_list_view_empty(self):
        with self.user('admin'):
            lst = api.content.create(
                id='test',
                type='seantis.people.list',
                container=self.new_temporary_folder()
            )

            view = lst.unrestrictedTraverse('@@view')
        
        self.assertIn('No people in the list.', view())
