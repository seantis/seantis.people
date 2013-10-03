from five import grok

from seantis.people.interfaces import IList
from seantis.people.browser import BaseView


class ListView(BaseView):

    permission = 'zope2.View'
    grok.require(permission)
    grok.context(IList)
    grok.name('view')

    template = grok.PageTemplateFile('templates/list.pt')

    def count(self):
        return len(self.context.people())
