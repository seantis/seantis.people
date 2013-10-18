from zope.schema import getFields
from seantis.plonetools.schemafields import Email, Website
from plone.namedfile.field import NamedBlobImage, NamedImage


class EmailFieldRenderer(object):

    template = u'<a href="mailto:{0}">{0}</a>'

    def __call__(self, context, field):
        return self.template.format(getattr(context, field))


class WebsiteFieldRenderer(object):

    template = u'<a href="{0}" target="_blank">{0}</a>'

    def __call__(self, context, field):
        return self.template.format(getattr(context, field))


class ImageRenderer(object):

    template = u'<img src="{0}" />'

    def __call__(self, context, field):
        img = getattr(context, field)
        if img:
            url = '/'.join((context.getURL(), '@@images', field, 'thumb'))
            return self.template.format(url)
        else:
            return u''


renderers = {
    Email: EmailFieldRenderer(),
    Website: WebsiteFieldRenderer(),
    NamedBlobImage: ImageRenderer(),
    NamedImage: ImageRenderer()
}


class Renderer(object):

    def __init__(self, schema):
        self.schema = schema
        self.fields = getFields(schema)

    def render(self, context, field):
        return self.get_renderer(field)(context, field)

    def get_renderer(self, field):
        fieldtype = type(self.fields[field])
        return renderers.get(fieldtype, getattr)
