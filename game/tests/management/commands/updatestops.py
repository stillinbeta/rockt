import os
import glob
from zipfile import ZipFile

from django.conf import settings
from django.core import management
from django.test import TestCase

from game.models import Stop
from game.tests.utils import temporary_settings
from updatecars import NullStream

THIS_DIR = os.path.dirname(__file__)
GTFS_SUBDIR = '/gtfs'
GTFS_ZIP = '/gtfs.zip'


class UpdateStopsTests(TestCase):
    def setUp(self):

        # Construct the zip manually each time, to make debugging
        # slightly less painful
        with ZipFile(THIS_DIR + GTFS_ZIP, 'w') as gtfszip:
            for txt in glob.glob(THIS_DIR + GTFS_SUBDIR + '/*.txt'):
                gtfszip.write(txt, os.path.basename(txt))
        with temporary_settings({'GTFS_URL': THIS_DIR + GTFS_ZIP}):
            management.call_command('updatestops', stdout=NullStream())

    def test_correct_number_stops_created(self):
        self.assertEquals(Stop.objects.count(), 3)

    def test_information_correct(self):
        expected_data = {'08121': {'route': 510,
                                    'description': ('SPADINA AVENUE AT '
                                    + 'DUNDAS STREET WEST FARSIDE').title(),
                                    'location': [-79.397997, 43.652513]},
                         '13672': {'route': 511,
                                    'description': ('BATHURST STREET AT FORT'
                                    ' YORK BOULEVARD').title(),
                                    'location': [-79.400459, 43.63868]},
                         '00217': {'route': 511,
                                    'description': ('BATHURST STREET AT'
                                    ' WELLINGTON STREET WEST').title(),
                                    'location': [-79.402051, 43.642576]}}
        for route, vals in expected_data.items():
            stop = Stop.objects.get(number=route)
            for key, val in vals.items():
                self.assertEquals(getattr(stop, key), val)

    #We don't need to test for invalids, as we've tested every item in the DB
    def tearDown(self):
        pass
        os.remove(THIS_DIR + GTFS_ZIP)
