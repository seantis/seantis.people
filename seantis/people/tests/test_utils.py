from plone import api

from seantis.people import tests
from seantis.people import utils


class TestUtils(tests.IntegrationTestCase):

    def test_get_parent(self):
        folder = self.new_temporary_folder(title='parent')

        with self.user('admin'):
            ms = api.content.create(
                id='test',
                type='seantis.people.membership',
                container=folder
            )

        brain = api.content.get('/'.join(ms.getPhysicalPath()))

        self.assertEqual(utils.get_parent(brain).title, 'parent')
        self.assertEqual(utils.get_parent(ms).title, 'parent')