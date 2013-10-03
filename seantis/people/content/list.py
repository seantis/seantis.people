from five import grok
from plone import api
from plone.dexterity.content import Container
from Products.CMFPlone.interfaces.constrains import IConstrainTypes, ENABLED

from seantis.people.interfaces import IPerson, IList
from seantis.people import utils


class List(Container):

    def people(self):
        catalog = api.portal.get_tool('portal_catalog')
        path = {'query': '/'.join(self.getPhysicalPath()), 'depth': 1}

        return catalog(path=path)

    def possible_types(self):
        return utils.get_type_info_by_behavior(IPerson.__identifier__)

    def available_types(self):
        used_type = self.used_type()
        
        if used_type:
            return [used_type]
        else:
            return self.possible_types()

    def used_type(self):
        catalog = api.portal.get_tool('portal_catalog')
        path = {'query': '/'.join(self.getPhysicalPath()), 'depth': 1}

        for fti in self.possible_types():
            if catalog(path=path, portal_type=fti.id, sort_limit=1)[:1]:
                return fti

        return None


class ListConstrainTypes(grok.Adapter):
    grok.provides(IConstrainTypes)
    grok.context(IList)

    def getConstrainTypesMode(self):
        return ENABLED

    def getLocallyAllowedTypes(self):
        return tuple(t.id for t in self.context.available_types())

    def allowedContentTypes(self):
        return self.context.available_types()

    def getImmediatelyAddableTypes(self):
        return self.getLocallyAllowedTypes()
