from plone.dexterity.content import Container
from plone.directives import form


class IPHZ(form.Schema):
    form.model("phz.xml")


class PHZ(Container):
    pass
