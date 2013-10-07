from plone import api

from Products.CMFPlone.interfaces.constrains import IConstrainTypes, ENABLED

from seantis.people.interfaces import IPerson
from seantis.people.content import List
from seantis.people import tests
from seantis.people.content.list import ListConstrainTypes

from pyquery import PyQuery as pq

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

    def test_list_constrain(self):
        with self.user('admin'):
            lst = api.content.create(
                id='test',
                type='seantis.people.list',
                container=self.new_temporary_folder()
            )
            constrain = IConstrainTypes(lst)

            new_type = self.new_temporary_type(
                behaviors=[IPerson.__identifier__]
            )

            self.assertIs(type(constrain), ListConstrainTypes)
            self.assertEqual(constrain.getConstrainTypesMode(), ENABLED)
            self.assertEqual(constrain.allowedContentTypes(), [new_type])
            self.assertEqual(constrain.getLocallyAllowedTypes(), [new_type.id])
            self.assertEqual(
                constrain.getImmediatelyAddableTypes(), [new_type]
            )

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

    def test_list_view_columns(self):

        model = """<?xml version='1.0' encoding='utf8'?>
        <model 
            xmlns="http://namespaces.plone.org/supermodel/schema"
            xmlns:people="http://namespaces.plone.org/supermodel/people"
        >
            <schema>
                <field
                    name="firstname" 
                    type="zope.schema.TextLine"
                    people:column="1">
                    <title>First name</title>
                </field>
                <field 
                    name="lastname" 
                    type="zope.schema.TextLine" 
                    people:column="2">
                    <title>Last name</title>
                </field>
            </schema>
        </model>"""

        with self.user('admin'):
            lst = api.content.create(
                id='test',
                type='seantis.people.list',
                container=self.new_temporary_folder(),
            )
            
            person = self.new_temporary_type(
                behaviors=[IPerson.__identifier__],
                model_source=model
            ).id
            
            api.content.create(id='miri', type=person, container=lst,
                firstname='Miriam', lastname='Linky'
            )
            api.content.create(id='zack', type=person, container=lst, 
                firstname='Zack', lastname='Brown'
            )

            view = lst.unrestrictedTraverse('@@view')

        page = pq(view())
        
        self.assertEqual(len(page.find('thead th')), 2)

        self.assertEqual(len(page.find('tbody tr')), 2)
        self.assertEqual(len(page.find('tbody tr:first-child td')), 2)

        self.assertEqual(page.find('thead').text(), 'First name Last name')
        self.assertEqual(page.find('tbody').text(), 'Miriam Linky Zack Brown')