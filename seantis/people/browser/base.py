from copy import copy

from five import grok
from z3c.form.browser.radio import RadioFieldWidget
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from seantis.plonetools.browser import BaseView as SharedBaseView
from seantis.plonetools.browser import BaseForm as SharedBaseForm

from seantis.people.interfaces import ISeantisPeopleSpecific


class BaseView(SharedBaseView):

    grok.baseclass()
    grok.layer(ISeantisPeopleSpecific)

    domain = 'seantis.people'


class BaseForm(SharedBaseForm):

    grok.baseclass()
    grok.layer(ISeantisPeopleSpecific)

    domain = 'seantis.people'


class ImportExportBaseForm(BaseForm):

    grok.baseclass()

    def available_types_vocabulary(self):
        translate = lambda txt: self.translate(unicode(txt))
        return SimpleVocabulary(terms=[
            SimpleTerm(fti.id, title=translate(fti.title)) for fti
            in self.context.available_types()
        ])

    def prepare_portal_type_field(self, fields):
        assert 'portal_type' in fields, "requires portal_type field"

        f = fields['portal_type']
        vocabulary = self.available_types_vocabulary()

        f.field = copy(f.field)
        f.field.vocabulary = vocabulary
        f.widgetFactory = RadioFieldWidget
        f.field.default = vocabulary._terms[0].value
