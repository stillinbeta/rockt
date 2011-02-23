# This file imports from GTFS datasets. The process is rather roundabout 
# due to lack of stop data by route. 

#Start out with the route numbers. In Toronto, this is 501 to 512

path_to_gtfs = '../data/'

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
        arr = stop[1:6] #this is route number, name, coordinates
        arr.append(stop_id_routes[stop[0]]) #this is our route number
        stop_set.add(tuple(arr))
stops.close()

for stop in stop_set:
    print stop

