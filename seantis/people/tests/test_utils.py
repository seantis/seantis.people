from App.config import getConfiguration, setConfiguration
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

    def test_in_debug_mode(self):
        cfg = getConfiguration()
        
        cfg.debug_mode = False
        setConfiguration(cfg)

        self.assertFalse(utils.in_debug_mode())

        cfg.debug_mode = True
        setConfiguration(cfg)

        self.assertTrue(utils.in_debug_mode())

    def test_is_existing_portal_type(self):
        new_type = self.new_temporary_type()

        self.assertTrue(utils.is_existing_portal_type(new_type.id))
        self.assertFalse(utils.is_existing_portal_type('inexistant'))
