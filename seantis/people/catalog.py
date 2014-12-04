from AccessControl import ClassSecurityInfo
from copy import copy, deepcopy
from Globals import InitializeClass
from plone import api
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ZCatalog.ZCatalog import ZCatalog
from seantis.people import catalog_id
from seantis.people.interfaces import IPeopleCatalog
from zope.interface import implements


def on_person_modified(obj, event=None):
    reindex_person(obj)


def reindex_person(obj, idxs=[]):
    catalog = api.portal.get_tool(catalog_id)
    catalog.reindexObject(obj, idxs=idxs)


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

        self._catalog.indexes = deepcopy(self.base_catalog._catalog.indexes)
        self._catalog.schema = copy(self.base_catalog._catalog.schema)
        self._catalog.names = copy(self.base_catalog._catalog.names)

    @property
    def plone_lexicon(self):
        return self.base_catalog.plone_lexicon

    @property
    def base_catalog(self):
        return api.portal.get_tool('portal_catalog')

    @property
    def unique_indexes(self):
        this = self._catalog.indexes.keys()
        base = self.base_catalog._catalog.indexes.keys()
        return set(this) - set(base)

    def catalog_object(self, obj, uid=None, idxs=None, update_metadata=1,
                       pghandler=None):
        if idxs:
            base_idxs = [ix for ix in idxs if ix not in self.unique_indexes]
        else:
            base_idxs = idxs

        self.base_catalog.catalog_object(
            obj, uid, base_idxs, update_metadata, pghandler
        )
        super(PeopleCatalog, self).catalog_object(
            obj, uid, idxs, update_metadata, pghandler
        )

    def uncatalog_object(self, *args, **kwargs):
        self.base_catalog.uncatalog_object(*args, **kwargs)
        super(PeopleCatalog, self).uncatalog_object(*args, **kwargs)


InitializeClass(PeopleCatalog)
