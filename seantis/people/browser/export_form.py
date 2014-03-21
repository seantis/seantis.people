from copy import copy

from five import grok
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from plone.directives import form

from seantis.people import _
from seantis.people.interfaces import IList
from seantis.people.browser import BaseForm
from seantis.people.content.export_content import (
    supported_formats, export_people
)

uppercase_formats = [f.upper() for f in supported_formats]


class IExportFormSchema(form.Schema):

    export_fields = schema.List(
        title=_(u"Fields"),
        description=_(u"Fields to include in the export"),
        required=True,
        value_type=schema.Choice(values=[]),
    )

    export_format = schema.Choice(
        title=_(u"Format"),
        values=uppercase_formats,
        default='CSV'
    )


class ExportForm(BaseForm):

    grok.require('cmf.ModifyPortalContent')
    grok.context(IList)
    grok.name('export')

    ignoreContext = True

    @property
    def label(self):
        return _(u"Export ${name}", mapping={
            'name': self.context.title
        })

    @property
    def portal_type(self):
        return self.context.used_type()

    @property
    def portal_type_fields(self):
        if self.portal_type:
            return field.Fields(self.portal_type.lookupSchema()).items()
        else:
            return []

    @property
    def fields(self):
        fields = field.Fields(IExportFormSchema)
        self.prepare_export_fields(fields)
        self.prepare_format_field(fields)
        return fields

    def prepare_export_fields(self, fields):

        vocabulary = SimpleVocabulary(terms=[
            SimpleTerm(id, title=self.translate(f.field.title)) for id, f
            in self.portal_type_fields
        ])

        default_values = [i[0] for i in self.portal_type_fields]

        f = fields['export_fields']
        f.field = copy(f.field)

        f.field.value_type.vocabulary = vocabulary
        f.field.default = default_values

        f.widgetFactory = CheckBoxFieldWidget

    def prepare_format_field(self, fields):
        f = fields['export_format']
        f.field = copy(f.field)
        f.widgetFactory = RadioFieldWidget

    @property
    def available_actions(self):
        yield dict(name='export', title=_(u"Export"), css_class='context')
        yield dict(name='cancel', title=_(u"Cancel"))

    def handle_export(self):
        export_people(
            self.request,
            self.context,
            self.parameters.get('portal_type'),
            self.parameters.get('export_format').lower(),
            self.parameters.get('export_fields')
        )
