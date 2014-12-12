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

    The catalog is used by all types that inherit from
    seantis.people.types.base.PersonBase. It is supposed to shadow the
    portal_catalog. It does so by applying indexing operations to both itself
    and the portal_catalog.

    This results in a separate catalog that has the same indexes and metadata
    as the portal_catalog plus additional indexes and metadata defined by the
    custom people types.

    This catalog can be used if all that is required is a lookup to people
    indexes/properties - like when displaying the list of people. Anything
    else should still go through portal_catalog.

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

        # copy the indexs of portal_catalog, so the code using this catalog
        # doesn't have to know where each index/metadata-column is stored
        self._catalog.indexes = deepcopy(self.base_catalog._catalog.indexes)
        self._catalog.schema = deepcopy(self.base_catalog._catalog.schema)
        self._catalog.names = deepcopy(self.base_catalog._catalog.names)

        # setup the lexicons as some Plone internal code depends on it
        lexicons = ('plone_lexicon', 'plaintext_lexicon', 'htmltext_lexicon')

        for lexicon in lexicons:
            self._setObject(lexicon, PLexicon(lexicon))

        # the catalog needs to be cleared after setting up the indexes
        # or they will encounter subtle errors (like print failing on brains)
        self._catalog.clear()
        self._catalog.updateBrains()

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
