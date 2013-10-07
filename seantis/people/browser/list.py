from five import grok

from seantis.people.interfaces import IList
from seantis.people.browser import BaseView
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

    @property
    def schema(self):
        used_type = self.context.used_type()

        assert used_type, """
            Do not use if there are no people in the list.
        """

        return used_type.lookupSchema()

    @property
    def filter(self):
        for key in self.request.keys():
            if key.startswith('select-'):
                return key.replace('select-', ''), self.request[key]

        return None

    def people(self):
        return self.context.people(filter=self.filter)

    def columns(self):
        return list(get_table_columns_merged(self.schema))

    def show_combobox(self, column):
        if len(column[1]) != 1:  # only columns with one attribute for now
            return False

        return column[1][0] in get_selectable_fields(self.schema)

    def combobox_values(self, column):
        return sorted(set(
            getattr(brain, column[1][0]) for brain in self.context.people()
        ))
