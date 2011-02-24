# This file imports from GTFS datasets. The process is rather roundabout 
# due to lack of stop data by route. The entire process is very
# inefficient, but it's destined to run once every few months. 
from models import Stop
import itertools


#Start out with the route numbers. In Toronto, this is 501 to 512

path_to_gtfs = 'data/' #this must be absolute 

#Start out with the route numbers. In Toronto, this is 501 to 512
route_nums = []
for i in range(501,513):
    route_nums.append(str(i))


trip_set= set() #We use a set to avoid duplicates
trip_routes = {} #Keep track of which route on which trip
trips = open(path_to_gtfs + 'trips.txt') 
for trip in trips:
    trip = trip.split(',')
    if trip[3][0:3] in route_nums: #trip[3] is route_name
        trip_set.add(trip[2]) #trip[2] is trip_id
        trip_routes[trip[2]] = trip[3][0:3] #store which route for which trip
trips.close()

stop_id_set = set()
stop_id_routes = {} #Continue to collect route information
stop_times = open(path_to_gtfs + 'stop_times.txt')
for stop_time in stop_times:
    stop_time = stop_time.split(',')
    if stop_time[0] in trip_set: #stop_time[0] is trip_id
        stop_id_set.add(stop_time[3]) #stop_time[3] is stop_id
        stop_id_routes[stop_time[3]] = trip_routes[stop_time[0]]
stop_times.close()

stop_set = set()
stops = open(path_to_gtfs + 'stops.txt')
for stop in stops:
    stop = stop.split(',')
    if stop[0] in stop_id_set:
        arr = itertools.chain(stop[1:3],stop[4:6],[stop_id_routes[stop[0]]])
        stop_set.add(tuple(arr))
stops.close()

print 'Content-Type: text/plain'

count = 0
for stop in stop_set:
    new_stop = Stop.get_or_insert(key_name='stop-'+stop[0])
    new_stop.num = stop[0]
    new_stop.desc = stop[1].title() #Make the description easy to read
    new_stop.location = "%s,%s" % (stop[2],stop[3])
    new_stop.route = int(stop[4])
    new_stop.put()
    count += 1
    print new_stop.desc + " imported."

print "importation complete. %d stops imported" % count
    

