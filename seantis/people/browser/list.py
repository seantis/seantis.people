from five import grok

from seantis.people.interfaces import IList
from seantis.people.browser import BaseView
from seantis.people.content.list import ListFilter
from seantis.people.supermodel import (
    get_table_columns_merged,
    get_selectable_fields
)


class ListView(BaseView):

    permission = 'zope2.View'
    grok.require(permission)
    grok.context(IList)
    grok.name('view')

    template = grok.PageTemplateFile('templates/list.pt')
    filter_prefix = 'filter-'

    @property
    def has_people(self):
        return bool(self.context.used_type())

    @property
    def schema(self):
        assert self.has_people, """
            Do not use if there are no people in the list.
        """

        return self.context.used_type().lookupSchema()

    @property
    def filter(self):
        for key in self.request.keys():
            if key.startswith(self.filter_prefix):
                val = self.request[key]
                key = key.replace(self.filter_prefix, '')

                field = self.has_people and self.schema.get(key, None) or None
                title = field and field.title or u''

                return ListFilter(key, val, title)

        return None

    @property
    def hide_table_header(self):
        return 'hide-table-header' in self.request

    def people(self):
        return self.context.people(filter=self.filter)

    def columns(self):
        return list(get_table_columns_merged(self.schema))

    def show_combobox(self, column):
        if not column.single_attribute:
            return False

        return column.attributes[0] in get_selectable_fields(self.schema)

    def combobox_values(self, column):
        return sorted(set(
            getattr(
                brain, column.attributes[0]
            ) for brain in self.context.people()
        ))
