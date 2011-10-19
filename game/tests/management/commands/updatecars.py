import os

from django.conf import settings
from django.core import management
from django.test import TestCase

from game.models import Car, FareInfo

XML_FILE = os.path.dirname(__file__) + '/test-updatecars.xml' 

#can't have any output clogging our unit testing
class NullStream:
    def write(self, string):
        pass

class UpdateCarsTests(TestCase):
    def setUp(self):
        settings.NEXTBUS_API_URL = XML_FILE
        settings.NEXTBUS_ROUTE_LIST = ["501","511"]
        management.call_command('updatecars',stdout=NullStream())

    def test_only_two_imported(self):
        self.assertEquals(Car.objects.count(),2)
        
    def test_other_routes_not_imported(self):
        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(number=1049)
        with self.assertRaises(Car.DoesNotExist):
            Car.objects.get(number=8217)
    def test_imported_data_correct(self):
        clrv = Car.objects.get(number=4095)
        self.assertEquals(clrv.route, 501)
        self.assertItemsEqual(clrv.location, [-79.445847, 43.638817])

        alrv = Car.objects.get(number=4212)
        self.assertEquals(alrv.route, 511)
        self.assertItemsEqual(alrv.location, [-79.281281, 43.673717])
    
    def test_old_cars_not_added_twice(self):
        management.call_command('updatecars',stdout=NullStream())
        self.assertEquals(Car.objects.count(),2)

    def test_car_not_in_update_marked_inactive(self):
        number = 4111
        Car.objects.create(number=number,
                           route=511,
                           location=(0,0),
                           active=True,
                           owner_fares=FareInfo(),
                           total_fares=FareInfo()) 
        management.call_command('updatecars',stdout=NullStream())
        self.assertFalse(Car.objects.get(number=number).active)
