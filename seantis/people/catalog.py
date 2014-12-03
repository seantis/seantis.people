from zope.interface import implements


from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from plone import api
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.CMFPlone.CatalogTool import CatalogTool

from seantis.people import catalog_id
from seantis.people.interfaces import IPeopleCatalog


def on_person_modified(obj, event=None):
    reindex_person(obj)


def reindex_person(obj):
    catalog = api.portal.get_tool(catalog_id)
    catalog.reindexObject(obj)


class PeopleCatalog(CatalogTool):
    """ A custom catalog for seantis.people. Required because people may have
    a large number of metadata/indicies assigned to them which would slow
    down the rest of the site.

    """

    implements(IPeopleCatalog)

    title = "Seantis People Catalog"
    id = catalog_id
    portal_type = meta_type = 'PeopleCatalog'
    plone_tool = 1

    security = ClassSecurityInfo()

    _properties = (
        {'id': 'title', 'type': 'string', 'mode': 'w'},
    )

    def __init__(self):
        ZCatalog.__init__(self, self.id)


InitializeClass(PeopleCatalog)
