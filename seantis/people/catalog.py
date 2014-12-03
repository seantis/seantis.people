from zope.interface import implements


from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.CMFPlone.CatalogTool import CatalogTool


from seantis.people.interfaces import IPeopleCatalog


class PeopleCatalog(CatalogTool):
    """ A custom catalog for seantis.people. Required because people may have
    a large number of metadata/indicies assigned to them which would slow
    down the rest of the site.

    """

    implements(IPeopleCatalog)

    title = "Seantis People Catalog"
    id = 'seantis_people_catalog'
    portal_type = meta_type = 'PeopleCatalog'
    plone_tool = 1

    security = ClassSecurityInfo()

    _properties = (
        {'id': 'title', 'type': 'string', 'mode': 'w'},
    )

    def __init__(self):
        ZCatalog.__init__(self, self.id)

    security.declarePublic('enumerateIndexes')

    def enumerateIndexes(self):
        """Returns indexes used by catalog"""
        return (
            ('id', 'FieldIndex', ()),
            ('portal_type', 'FieldIndex', ()),
            ('path', 'ExtendedPathIndex', ('getPhysicalPath')),
            ('getCanonicalPath', 'ExtendedPathIndex', ('getCanonicalPath')),
            ('isArchived', 'FieldIndex', ()),
            ('is_trashed', 'FieldIndex', ()),
            ('is_obsolete', 'FieldIndex', ()),
            ('Language', 'FieldIndex', ()),
            ('review_state', 'FieldIndex', ()),
            ('allowedRolesAndUsers', 'DPLARAUIndex', ()),
        )

    security.declarePublic('enumerateMetadata')

    def enumerateMetadata(self):
        """Returns metadata used by catalog"""
        return (
            'Title',
            'getId',
            'UID',
            'review_state',
            'created',
            'modified',
        )

    security.declareProtected(ManagePortal, 'clearFindAndRebuild')

    def clearFindAndRebuild(self):
        """Empties catalog, then finds all contentish objects (i.e. objects
           with an indexObject method), and reindexes them.
           This may take a long time.
        """

        def indexObject(obj, path):
            self.reindexObject(obj)

        self.manage_catalogClear()

        portal = getToolByName(self, 'portal_url').getPortalObject()
        import pdb; pdb.set_trace()
        portal.ZopeFindAndApply(
            portal, obj_metatypes=(), search_sub=True, apply_func=indexObject
        )

InitializeClass(PeopleCatalog)
