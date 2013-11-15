from collections import namedtuple
from plone import api
from five import grok
from zope.interface import Interface

from seantis.plonetools import tools
from seantis.people.browser.base import BaseView
from seantis.people.interfaces import IPerson


class View(BaseView):
    """A numer of macros for use with seantis.people"""

    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('seantis-people-macros')

    template = grok.PageTemplateFile('templates/macros.pt')

    def __getitem__(self, key):
        return self.template._template.macros[key]

    def organizations(self, person):
        Organization = namedtuple('Organization', ['title', 'url'])

        catalog = api.portal.get_tool('portal_catalog')

        organizations = []
        for uuid in IPerson(self.context).memberships():
            brain = catalog(UID=uuid)[0]
            organizations.append(Organization(brain.Title, brain.getURL()))

        sortkey = lambda org: tools.unicode_collate_sortkey()(org.title)

        return sorted(organizations, key=sortkey)
