
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form

from z3c.relationfield.schema import RelationChoice

from zope import schema
from zope.interface import Interface, invariant, Invalid

from seantis.people import _

# NameFromPerson Field Key
NAME_FROM_PERSON = u'seantis.people.name_from_person'

# Person Column Field Key
PERSON_COLUMNS = u'seantis.people.person_column'

# Supermodel namespace and prefix
PEOPLE_NAMESPACE = 'http://namespaces.plone.org/supermodel/people'
PEOPLE_PREFIX = 'people'


class ISeantisPeopleLayer(Interface):
    pass


class IPerson(Interface):

    def memberships(self):
        """ A list of membership belonging to this person. """

    def memberships_by_organizations(self, organizations=None):
        """ A dictionary of memberships belonging to this person. They key
        of the dictionary is the title of the organization. """


class INameFromPerson(Interface):
    pass


class IList(form.Schema):
    """ A list of IPerson objects. """

    title = schema.TextLine(
        title=_(u"Name of the list of people"),
        required=True
    )


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

    person = RelationChoice(
        title=_(u"Person"),
        source=ObjPathSourceBinder(object_provides=IPerson.__identifier__),
        required=True,
    )

    @invariant
    def has_valid_daterange(Membership):
        if Membership.start is None:
            return

        if Membership.end is None:
            return

        if Membership.start > Membership.end:
            raise Invalid(_(u"The membership can't end before it starts" ))
