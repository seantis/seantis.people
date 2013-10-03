from plone import api

from seantis.people.content import List
from seantis.people import tests


class TestList(tests.IntegrationTestCase):

    def test_list_creation(self):
        with self.user('admin'):
            ms = api.content.create(
                id='test',
                type='seantis.people.list',
                container=self.new_temporary_folder()
            )

        self.assertIs(type(ms.aq_base), List)
