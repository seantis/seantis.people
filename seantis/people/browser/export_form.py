from copy import copy

from five import grok
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.directives import form

from seantis.people import _
from seantis.people.interfaces import IList
from seantis.people.browser import ImportExportBaseForm


class IExportFormSchema(form.Schema):

    portal_type = schema.Choice(title=_(u"Type"), values=[])

    export_fields = schema.List(
        title=u"Fields",
        description=u"Fields to include in the export",
        required=True,
        value_type=schema.Choice(values=[]),
    )


class ExportForm(ImportExportBaseForm):

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
        portal_type = self.request.get('portal_type')
        valid_portal_types = [t for t in self.context.available_types()]

        for fti in valid_portal_types:
            if fti.id == portal_type:
                return fti

        return valid_portal_types[0]

    @property
    def portal_type_fields(self):
        return field.Fields(self.portal_type.lookupSchema()).items()

    @property
    def fields(self):
        fields = field.Fields(IExportFormSchema)
        self.prepare_portal_type_field(fields)
        self.prepare_export_fields(fields)
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

    @property
    def available_actions(self):
        yield dict(name='export', title=_(u"Export"), css_class='context')
        yield dict(name='cancel', title=_(u"Cancel"))

    def handle_export(self):
        print self.parameters
        print 'aww yeah'
