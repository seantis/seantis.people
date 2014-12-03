from plone import api
from plone.dexterity.content import Container
from seantis.people.interfaces import IPerson
from seantis.people import _
from seantis.people import catalog_id


class PersonBase(Container):

    def _getCatalogTool(self):
        return api.portal.get_tool(catalog_id)

    @property
    def memberships(self):
        return IPerson(self).memberships()

    @property
    def organizations(self):
        return IPerson(self).organizations()

    @property
    def organization_uuids(self):
        return IPerson(self).organization_uuids()

    @property
    def membership_fields(self):
        return {
            'memberships': _(u'Memberships')
        }
