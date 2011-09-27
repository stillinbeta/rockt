from django.core.management import setup_environ
import settings
setup_environ(settings)

from rockt.cars.update import update_streetcars, remove_out_of_service

routes = range(501,513)
route_list = []
for route in routes:
    route_list.append(str(route)) 

cars_updated = update_streetcars(route_list)
print "Update is Complete, %d cars in service" % len(cars_updated)
remove_out_of_service(cars_updated)
print "Removal Complete"
