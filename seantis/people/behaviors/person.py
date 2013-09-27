from plone import api
from zope.interface import implements

from seantis.people import tools
from seantis.people.interfaces import IPerson

class Person(object):
    implements(IPerson)

    def __init__(self, context):
        self.context = context

    def memberships(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        memberships = catalog(portal_type='seantis.people.membership')

        return memberships

    def memberships_by_organization(self, organizations=None):
        result = {}

        for membership in self.memberships():
            organization = tools.get_parent(membership).title

            if organizations is not None:
                if organization not in organizations:
                    continue

            if organization in result:
                result[organization].append(membership)
            else:
                result[organization] = [membership]

        return result
