from zope.schema import getFields
from seantis.plonetools.schemafields import Email, Website


class EmailFieldRenderer(object):

    template = u'<a href="mailto:{0}">{0}</a>'

    def __call__(self, value):
        return self.template.format(value)


class WebsiteFieldRenderer(object):

    template = u'<a href="{0}" target="_blank">{0}</a>'

    def __call__(self, value):
        return self.template.format(value)

renderers = {
    Email: EmailFieldRenderer(),
    Website: WebsiteFieldRenderer()
}


class Renderer(object):

    def __init__(self, schema):
        self.schema = schema
        self.fields = getFields(schema)

    def render(self, field, value):
        return self.get_renderer(field)(value)

    def get_renderer(self, field):
        fieldtype = type(self.fields[field])
        return renderers.get(fieldtype, lambda value: value)
