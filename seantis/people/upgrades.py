# -*- coding: utf-8 -*-

from zope.component import getUtility

from plone import api
from plone.dexterity.interfaces import IDexterityFTI

from seantis.people.supermodel.indexing import update_related_indexes


def import_profile(profile):
    setup = api.portal.get_tool('portal_setup')
    setup.runAllImportStepsFromProfile(profile)


def run_import_step_from_profile(step, module, profile):
    setup = api.portal.get_tool('portal_setup')
    profile = 'profile-{}:{}'.format(module, profile)
    setup.runImportStepFromProfile(profile, step)


def upgrade_portal_type(portal_type, module, profile):
    run_import_step_from_profile('typeinfo', module, profile)
    update_related_indexes(getUtility(IDexterityFTI, portal_type))


def install_custom_controlpanel(context):
    run_import_step_from_profile('controlpanel', 'seantis.people', 'default')


def upgrade_membership_title(context):
    upgrade_portal_type(
        'seantis.people.membership', 'seantis.people', 'default'
    )

    catalog = api.portal.get_tool('portal_catalog')
    memberships = catalog.unrestrictedSearchResults(
        portal_type='seantis.people.membership'
    )

    for membership in [m.getObject() for m in memberships]:
        if not hasattr(membership, 'role') or membership.role is None:
            membership.role = membership.title
            membership.title = membership.get_custom_title()
            membership.reindexObject()

            old_id = membership.id
            safe_title = membership.title.replace(u'ä', u'ae')
            safe_title = safe_title.replace(u'ö', u'oe')
            safe_title = safe_title.replace(u'ü', u'ue')

            new_id = safe_title.encode('ascii', 'ignore')
            new_id = new_id.lower().replace(' ', '-')
            membership.aq_inner.aq_parent.manage_renameObject(old_id, new_id)


def upgrade_phz_type_info(context):
    upgrade_portal_type('seantis.people.phz', 'seantis.people', 'phz')


def install_membership_dependencies(context):
    import_profile('profile-plone.formwidget.autocomplete:default')
    import_profile('profile-plone.app.relationfield:default')
