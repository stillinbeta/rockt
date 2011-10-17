# This file imports from GTFS datasets. The process is rather roundabout 
# due to lack of stop data by route. The entire process is very
# inefficient, but it's destined not to run very often 
import itertools
import tempfile
from urllib import urlopen
from zipfile import ZipFile
from shutil import rmtree

from django.core.management.base import BaseCommand
from django.conf import settings

from game.models import Stop

class Command(BaseCommand):
    help = 'Update the location data for the stops'

    def handle(self, *args, **kwargs):
        self.stdout.write("Downloading stops\n")

        tmpdir = tempfile.mkdtemp()
        path_to_gvfs = ''
        try:
            self.retrieve_data(tmpdir)
            self.stdout.write("Download complete\n")
            self.update_stops(tmpdir)
        finally:
            rmtree(tmpdir)

    def retrieve_data(self,tmpdir):
        gtfs_url = settings.GTFS_URL
        datafilename = tmpdir + '/data.zip'
        datafile = open(datafilename,'w') 
        request = urlopen(gtfs_url)
        for line in request:
            datafile.write(line)
        datafile.close() 

        archive = ZipFile(datafilename)
        archive.extractall(tmpdir)
        archive.close()
        

    def update_stops(self,path_to_gtfs):
        #Start out with the route numbers. In Toronto, this is 501 to 512
        route_nums = []
        for i in range(501,513):
            route_nums.append(str(i))


        trip_set= set() #We use a set to avoid duplicates
        trip_routes = {} #Keep track of which route on which trip
        trips = open(path_to_gtfs + '/trips.txt') 
        for trip in trips:
            trip = trip.split(',')
            if trip[3][0:3] in route_nums: #trip[3] is route_name
                trip_set.add(trip[2]) #trip[2] is trip_id
                #store which route for which trip
                trip_routes[trip[2]] = trip[3][0:3] 
        trips.close()

        stop_id_set = set()
        stop_id_routes = {} #Continue to collect route information
        stop_times = open(path_to_gtfs + '/stop_times.txt')
        for stop_time in stop_times:
            stop_time = stop_time.split(',')
            if stop_time[0] in trip_set: #stop_time[0] is trip_id
                stop_id_set.add(stop_time[3]) #stop_time[3] is stop_id
                stop_id_routes[stop_time[3]] = trip_routes[stop_time[0]]
        stop_times.close()

        stop_set = set()
        stops = open(path_to_gtfs + '/stops.txt')
        for stop in stops:
            stop = stop.split(',')
            if stop[0] in stop_id_set:
                arr = itertools.chain(stop[1:3],
                                      stop[4:6],
                                      [stop_id_routes[stop[0]]])
                stop_set.add(tuple(arr))
        stops.close()

        count = 0
        Stop.objects.all().delete()
        for stop in stop_set:
            new_stop = Stop()
            new_stop.number = stop[0]
            #Make the description easy to read
            new_stop.description = stop[1].title() 
            #MongoDB indices are lon/lat
            new_stop.location = (float(stop[3]),float(stop[2])) 
            new_stop.route = int(stop[4])
            new_stop.save()
            count += 1
            self.stdout.write(new_stop.description + " imported.\n")

        self.stdout.write("importation complete. %d stops imported\n" % count)
