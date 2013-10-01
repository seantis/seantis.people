from App.config import getConfiguration
from plone import api
from plone.dexterity.fti import (
    register as register_dexterity_type,
    DexterityFTI
)
from plone.dexterity.interfaces import IDexterityFTI
from Products.ZCatalog.interfaces import ICatalogBrain
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.schema import getFields


def get_parent(obj):
    """ Gets the parent of the obj or brain. """
    
    if ICatalogBrain.providedBy(obj):
        return api.content.get(path='/'.join(obj.getPath().split('/')[:-1]))
    else:
        return obj.aq_inner.aq_parent


def is_existing_portal_type(portal_type):
    try:
        getUtility(IDexterityFTI, portal_type)
    except ComponentLookupError:
        return False

    return True


def get_schema_from_portal_type(portal_type):
    """ Get the schema from a portal type. """

    fti = getUtility(IDexterityFTI, portal_type)
    return fti.lookupSchema()


def order_fields_by_schema_appearance(fields, schema):

     order = dict((key, f.order) for key, f in getFields(schema).items())
     return sorted(fields, key=order.get)


def add_attribute_to_metadata(attribute):
    zcatalog = api.portal.get_tool('portal_catalog')._catalog

    if attribute not in zcatalog.schema:
        zcatalog.addColumn(attribute)


def get_brain_by_object(obj):
    """ The inverse of getObject. """
    catalog = api.portal.get_tool('portal_catalog')

    return catalog(path={'query': '/'.join(obj.getPhysicalPath())})[0]


def in_debug_mode():
    return getConfiguration().debug_mode


def add_new_dexterity_type(name, **kwargs):
    new_type = DexterityFTI(name)
    kwargs['klass'] = 'plone.dexterity.content.Container'

    if 'behaviors' in kwargs:
        if isinstance(kwargs['behaviors'], list):
            kwargs['behaviors'] = '\n'.join(kwargs['behaviors'])
    
    new_type.manage_changeProperties(
        **kwargs
    )

    types = api.portal.get_tool('portal_types')
    types._setObject(new_type.id, new_type)

    register_dexterity_type(new_type)

    return new_type
