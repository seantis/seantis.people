from five import grok

from seantis.plonetools import tools
from seantis.people.supermodel import security, get_detail_fields
from seantis.people.interfaces import IPersonMarker
from seantis.people.browser import BaseView, Renderer


class ListView(BaseView):

    permission = 'zope2.View'
    grok.require(permission)
    grok.context(IPersonMarker)
    grok.name('view')

    template = grok.PageTemplateFile('templates/person.pt')

    def update(self):
        self.renderer = Renderer(self.schema)

    @property
    def schema(self):
        return tools.get_schema_from_portal_type(self.context.portal_type)

    def fields(self):
        has_access = lambda field: security.has_read_access(
            self.schema, field, self.context
        )
        return [f for f in get_detail_fields(self.schema) if has_access(f)]

    def get_field_title(self, field):
        if field in self.schema:
            return self.schema[field].title
        else:
            return field
