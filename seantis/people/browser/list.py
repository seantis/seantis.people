from plone import api
from five import grok

from seantis.people.interfaces import IList, IPerson
from seantis.people.browser import BaseView
from seantis.people import utils


class ListView(BaseView):

    permission = 'zope2.View'
    grok.require(permission)
    grok.context(IList)
    grok.name('view')

    template = grok.PageTemplateFile('templates/list.pt')

    def count(self):
        return len(self.people())

    def types(self):
        return utils.get_type_info_by_behavior(IPerson.__identifier__)

    def people(self):
        catalog = api.portal.get_tool('portal_catalog')

        return catalog(
            path={
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1
            },
            portal_type=(t.id for t in self.types())
        )
