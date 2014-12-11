from AccessControl import ClassSecurityInfo
from copy import deepcopy
from Globals import InitializeClass
from plone import api
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.ZCTextIndex.ZCTextIndex import PLexicon
from seantis.people import catalog_id
from seantis.people.interfaces import IPeopleCatalog
from zope.interface import implements


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
        self._catalog.schema = deepcopy(self.base_catalog._catalog.schema)
        self._catalog.names = deepcopy(self.base_catalog._catalog.names)

        lexicons = ('plone_lexicon', 'plaintext_lexicon', 'htmltext_lexicon')

        for lexicon in lexicons:
            self._setObject(lexicon, PLexicon(lexicon))

        self._catalog.clear()  # the catalog needs to be cleared after setting
                               # up the indexes, or there will be problems

    @property
    def base_catalog(self):
        return api.portal.get_tool('portal_catalog')

    security.declarePrivate('indexObject')
    security.declarePrivate('reindexObject')
    security.declarePrivate('unindexObject')

    def indexObject(self, *args, **kwargs):
        self.base_catalog.indexObject(*args, **kwargs)
        super(PeopleCatalog, self).indexObject(*args, **kwargs)

    def reindexObject(self, *args, **kwargs):
        self.base_catalog.reindexObject(*args, **kwargs)
        super(PeopleCatalog, self).reindexObject(*args, **kwargs)

    def unindexObject(self, *args, **kwargs):
        self.base_catalog.unindexObject(*args, **kwargs)
        super(PeopleCatalog, self).unindexObject(*args, **kwargs)


InitializeClass(PeopleCatalog)
