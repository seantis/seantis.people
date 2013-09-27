from plone import api

from seantis.people import tests
from seantis.people import tools


class TestTools(tests.IntegrationTestCase):

    def test_get_parent(self):
        folder = self.new_temporary_folder(title='parent')

        with self.user('admin'):
            ms = api.content.create(
                id='test',
                type='seantis.people.membership',
                container=folder
            )

        brain = api.content.get('/'.join(ms.getPhysicalPath()))

        self.assertEqual(tools.get_parent(brain).title, 'parent')
        self.assertEqual(tools.get_parent(ms).title, 'parent')