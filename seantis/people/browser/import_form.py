import transaction
from five import grok

from zope import schema
from z3c.form import field
from plone.directives import form
from plone.namedfile.field import NamedFile

from seantis.people import _
from seantis.people.errors import ContentImportError
from seantis.people.interfaces import IList
from seantis.people.browser import ImportExportBaseForm
from seantis.people.content.import_content import (
    supported_formats,
    import_people
)


class IImportFormSchema(form.Schema):

    portal_type = schema.Choice(title=_(u"Type"), values=[])
    import_file = NamedFile(title=_(u"File"))


class ImportForm(ImportExportBaseForm):

    grok.require('cmf.ManagePortal')
    grok.context(IList)
    grok.name('import')

    ignoreContext = True

    @property
    def label(self):
        return _(u"Import ${name}", mapping={
            'name': self.context.title
        })

    @property
    def fields(self):
        fields = field.Fields(IImportFormSchema)
        self.prepare_portal_type_field(fields)
        return fields

    @property
    def available_actions(self):
        yield dict(name='import', title=_(u'Import'), css_class='context')
        yield dict(name='cancel', title=_(u'Cancel'))

    def get_format_from_filename(self, filename):
        if '.' in filename:
            return filename.split('.')[-1]
        else:
            return ''

    def handle_import(self):
        if not self.parameters:
            return

        try:
            portal_type = self.parameters['portal_type']
            import_file = self.parameters['import_file']

            format = self.get_format_from_filename(import_file.filename)

            if not format in supported_formats:
                raise ContentImportError(_(
                    u'${format} is not supported, supported are ${formats}',
                    mapping={
                        'format': format,
                        'formats': ', '.join(supported_formats)
                    }
                ))

            count = import_people(
                self.request,
                self.context,
                portal_type,
                format,
                import_file.data
            )

            self.status = _(
                u'Successfully imported ${count} records', mapping=dict(
                    count=count
                )
            )
        except ContentImportError, e:
            transaction.abort()
            self.raise_action_error(e.translate(self.request))
        else:
            self.request.response.redirect(self.context.absolute_url())
