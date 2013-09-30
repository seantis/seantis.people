
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from Products.ZCatalog.interfaces import ICatalogBrain
from zope.component import getUtility


def get_parent(obj):
    """ Gets the parent of the obj or brain. """
    
    if ICatalogBrain.providedBy(obj):
        return api.content.get(path='/'.join(obj.getPath().split('/')[:-1]))
    else:
        return obj.aq_inner.aq_parent


def get_schema_from_portal_type(portal_type):
    """ Get the schema from a portal type. """

    fti = getUtility(IDexterityFTI, portal_type)
    return fti.lookupSchema()
