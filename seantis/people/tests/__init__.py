import unittest2 as unittest

from zope import event
from zope.security.management import newInteraction, endInteraction

from zope.component import getSiteManager
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

from plone.app.testing import login, logout

from collective.betterbrowser import new_browser

from seantis.people.testing import (
    INTEGRATION_TESTING,
    FUNCTIONAL_TESTING
)


def install_mailhost(portal, mailhost):
    portal.MailHost = mailhost

    sm = getSiteManager(context=portal)
    sm.unregisterUtility(provided=IMailHost)
    sm.registerUtility(mailhost, provided=IMailHost) 


def install_mock_mailhost(portal, from_address='noreply@example.com'):
    portal._original_mailhost = portal.MailHost
    portal.email_from_address = from_address
    install_mailhost(portal, MockMailHost())


def uninstall_mock_mailhost(portal):
    if hasattr('_original_mailhost', portal):
        install_mailhost(portal, portal._original_mailhost)


class TestCase(unittest.TestCase):

    def setUp(self):

        self.app = self.layer['app']
        self.portal = self.layer['portal']

        install_mock_mailhost(self.portal)

        # remove all test event subscribers
        event.subscribers = [
            e for e in event.subscribers if type(e) != TestEventSubscriber
        ]

    def tearDown(self):
        uninstall_mock_mailhost(self.portal)
        self.logout()

    @property
    def request(self):
        return self.layer['request']

    @property
    def mailhost(self):
        return self.portal.MailHost

    def login(self, user):
        login(user)

    def logout(self):
        logout()

    def new_browser(self):
        return new_browser(self.layer)

    def subscribe(self, eventclass):
        subscriber = TestEventSubscriber(eventclass)
        event.subscribers.append(subscriber)
        return subscriber


class TestEventSubscriber(object):

    def __init__(self, eventclass):
        self.eventclass = eventclass
        self.event = None

    def __call__(self, event):
        if type(event) is self.eventclass:
            self.event = event

    def was_fired(self):
        return self.event is not None

    def reset(self):
        self.event = None


# to use with integration where security interactions need to be done manually
class IntegrationTestCase(TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        # setup security
        newInteraction()

    def tearDown(self):
        endInteraction()
        super(IntegrationTestCase, self).tearDown()


# to use with the browser which does its own security interactions
class FunctionalTestCase(TestCase):
    layer = FUNCTIONAL_TESTING