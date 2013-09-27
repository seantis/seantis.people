from plone import api
from Products.ZCatalog.interfaces import ICatalogBrain


def get_parent(obj):
    """ Gets the parent of the obj or brain. """
    
    if ICatalogBrain.providedBy(obj):
        return api.content.get(path='/'.join(obj.getPath().split('/')[:-1]))
    else:
        return obj.aq_inner.aq_parent
