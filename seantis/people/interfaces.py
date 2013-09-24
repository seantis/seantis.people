
from plone.directives import form

from zope import schema
from zope.interface import Interface, invariant, Invalid

from seantis.people import _


class ISeantisPeopleLayer(Interface):
    pass


class IPerson(Interface):
    pass


class IMembership(form.Schema):

    title = schema.TextLine(
        title=_(u"Role inside organization"),
        required=True
    )

    start = schema.Date(
        title=_(u"Start of membership"),
        required=False
    )

    end = schema.Date(
        title=_(u"End of membership"),
        required=False
    )

    @invariant
    def has_valid_daterange(Membership):
        if Membership.start is None:
            return

        if Membership.end is None:
            return

        if Membership.start > Membership.end:
            raise Invalid(_(u"The membership can't end before it starts" ))
