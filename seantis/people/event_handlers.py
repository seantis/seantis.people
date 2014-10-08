from five import grok
from plone import api
from ZPublisher.interfaces import IPubBeforeCommit


@grok.subscribe(IPubBeforeCommit)
def reindex_lists(event):
    if event.request.URL.endswith('manage_catalogRebuild'):
        catalog = api.portal.get_tool('portal_catalog')

        lists = catalog.unrestrictedSearchResults(
            portal_type='seantis.people.list'
        )

        for brain in lists:
            brain.getObject().reindex_organisations()
