from datetime import date
from plone import api
from zope.interface import Invalid

from seantis.people.interfaces import IMembership
from seantis.people.content import Membership
from seantis.people import tests


class TestMembership(tests.IntegrationTestCase):

    def test_membership_creation(self):
        with self.user('admin'):
            ms = api.content.create(
                id='test',
                type='seantis.people.membership',
                container=self.new_temporary_folder()
            )

        self.assertIs(type(ms.aq_base), Membership)

    def test_membership_range_validation(self):
        with self.user('admin'):
            ms = api.content.create(
                id='test',
                type='seantis.people.membership',
                container=self.new_temporary_folder()
            )

        ms.start, ms.end = None, None
        IMembership.validateInvariants(ms)

        ms.start, ms.end = date(2012, 1, 1), None
        IMembership.validateInvariants(ms)

        ms.start, ms.end = None, date(2012, 1, 1)
        IMembership.validateInvariants(ms)

        ms.start, ms.end = date(2012, 1, 1), date(2012, 1, 2)
        IMembership.validateInvariants(ms)

        ms.start, ms.end = date(2012, 1, 1), date(2012, 1, 1)
        IMembership.validateInvariants(ms)

        ms.start, ms.end = date(2012, 1, 2), date(2012, 1, 1)
        self.assertRaises(Invalid, IMembership.validateInvariants, ms)
