import logging
log = logging.getLogger('seantis.people')

from zipfile import ZipFile

import csv
import os.path
import inspect

from StringIO import StringIO
from urllib2 import urlopen

from five import grok
from plone import api

from seantis.people.browser import BaseView
from seantis.people.interfaces import IList
from seantis.plonetools import utils


class LoadTestRecordsView(BaseView):

    permission = 'cmf.ManagePortal'
    grok.require(permission)

    grok.context(IList)
    grok.name('load-test-records')

    typename = 'test-record'

    @property
    def count(self):
        return self.request.get('count', '500')

    @property
    def url(self):
        return 'http://www.briandunning.com/sample-data/{}.zip'.format(
            self.count
        )

    @property
    def csv(self):
        return '{}.csv'.format(self.count)

    def load_xml(self):
        path = os.path.dirname(
            os.path.abspath(
                inspect.getfile(inspect.currentframe())
            )
        )

        return open(os.path.join(path, 'load_test_records.xml'), 'r').read()

    def create_type(self):
        if utils.is_existing_portal_type(self.typename):
            return

        utils.add_new_dexterity_type(
            self.typename, model_source=self.load_xml(),
            title=u'Test Record',
            behaviors=[
                'seantis.people.interfaces.IPerson',
                'seantis.people.interfaces.INameFromPerson'
            ]
        )

    def import_sample_data(self):
        zipfile = ZipFile(StringIO(urlopen(self.url).read()))

        # get rid of windows newlines - there's probably a more efficient way
        content = '\n'.join(zipfile.open(self.csv).read().splitlines())
        reader = csv.reader(StringIO(content), delimiter=',')

        headers = None

        for rowix, row in enumerate(reader):
            if not headers:
                headers = [key.lower() for key in row]
            else:
                kwargs = dict(
                    (header, row[ix]) for ix, header in enumerate(headers)
                )

                api.content.create(
                    id='',
                    type=self.typename,
                    container=self.context,
                    **kwargs
                )

        return rowix

    def render(self):
        if not utils.in_debug_mode():
            return "zope must be run in debug mode for this to work"

        RESPONSE = self.request.RESPONSE
        RESPONSE.setHeader('Content-Type', 'text/plain;charset=utf-8')

        log.info('creating type')
        self.create_type()

        log.info('importing sample data')
        rows = self.import_sample_data()

        log.info('imported {} records'.format(rows))
        self.request.response.redirect(self.context.absolute_url())
