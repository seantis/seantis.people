from plone import api

from seantis.people.interfaces import IPerson
from seantis.people import utils

from plone.dexterity.content import Container

class List(Container):

    def people(self):
        catalog = api.portal.get_tool('portal_catalog')

        types = utils.get_type_info_by_behavior(IPerson.__identifier__)
        path = {'query': '/'.join(self.getPhysicalPath()), 'depth': 1}

        return catalog(path=path, portal_type=tuple(t.id for t in types))
