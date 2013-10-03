from plone import api

from five import grok

from seantis.people.interfaces import IPerson, IList
from seantis.people.supermodel import get_table_columns
from seantis.people import utils

from plone.dexterity.content import Container
from Products.CMFPlone.interfaces.constrains import IConstrainTypes, ENABLED


class List(Container):

    def people(self):
        catalog = api.portal.get_tool('portal_catalog')
        path = {'query': '/'.join(self.getPhysicalPath()), 'depth': 1}

        return catalog(
            path=path, 
            portal_type=tuple(fti.id for fti in self.possible_types())
        )

    def possible_types(self):
        return utils.get_type_info_by_behavior(IPerson.__identifier__)

    def available_types(self):
        used_types = self.used_types()
        possible_types = self.possible_types()
        
        if not used_types:
            return possible_types

        existing_columns = get_table_columns(used_types[0].lookupSchema())

        available = []
        for fti in possible_types:
            if get_table_columns(fti.lookupSchema()) == existing_columns:
                available.append(fti)

        return available

    def used_types(self):
        catalog = api.portal.get_tool('portal_catalog')
        path = {'query': '/'.join(self.getPhysicalPath()), 'depth': 1}

        used_types = []

        for fti in self.possible_types():
            if catalog(path=path, portal_type=fti.id, sort_limit=1)[:1]:
                used_types.append(fti)

        return used_types


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
