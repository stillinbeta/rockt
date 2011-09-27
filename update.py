from os import getcwd
from shutil import rmtree
import argparse

from django.core.management import setup_environ
import settings
setup_environ(settings)

from rockt.cars.update import update_streetcars, remove_out_of_service
from rockt.stops.update import update_stops, retrieve_data 

def run_car_updater():
    routes = range(501,513)
    route_list = []
    for route in routes:
        route_list.append(str(route)) 

    cars_updated = update_streetcars(route_list)
    print "Update is Complete, %d cars in service" % len(cars_updated)
    remove_out_of_service(cars_updated)
    print "Removal Complete"

def run_stop_updater():
    print 'Downloading stops'
    path_to_gvfs = retrieve_data()
    print 'Download complete'
    update_stops(path_to_gvfs)
    rmtree(path_to_gvfs)

parser = argparse.ArgumentParser(description='Update external datasets')
parser.add_argument('--cars',
                    action='store_true',
                    help='Update streetcar location data')
parser.add_argument('--stops',
                    action='store_true',
                    help= 'Update stop location data')

opts = parser.parse_args()
if opts.cars:
    run_car_updater()
if opts.stops:
    run_stop_updater()


