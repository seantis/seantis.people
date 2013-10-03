from plone import api

from five import grok

from seantis.people.interfaces import IPerson, IList
from seantis.people import utils

from plone.dexterity.content import Container
from Products.CMFPlone.interfaces.constrains import IConstrainTypes, ENABLED


class List(Container):

    def people(self):
        catalog = api.portal.get_tool('portal_catalog')
        path = {'query': '/'.join(self.getPhysicalPath()), 'depth': 1}

        return catalog(
            path=path, portal_type=tuple(t.id for t in self.possible_types())
        )

    def possible_types(self):
        return utils.get_type_info_by_behavior(IPerson.__identifier__)

    def used_types(self):
        catalog = api.portal.get_tool('portal_catalog')
        path = {'query': '/'.join(self.getPhysicalPath()), 'depth': 1}

        used_types = []

        for portal_type in (t.id for t in self.possible_types()):
            if catalog(path=path, portal_type=portal_type, sort_limit=1)[:1]:
                used_types.append(portal_type)

        return used_types


class ListConstrainTypes(grok.Adapter):
    grok.provides(IConstrainTypes)
    grok.context(IList)

    def getConstrainTypesMode(self):
        return ENABLED

    def getLocallyAllowedTypes(self):
        return tuple(t.id for t in self.context.possible_types())

    def allowedContentTypes(self):
        return self.context.possible_types()

    def getImmediatelyAddableTypes(self):
        return self.getLocallyAllowedTypes()
