from geopy.distance import distance

def find_fare(user, car, on, off):
    if car.owner == user.get_profile():
        return 0
    
    #simple rules - CLRVs half as much and ALRVs
    CLRV_PRICE = 2
    ALRV_PRICE = 4
    
    #CLRVs are 40,41, ALRVs are 42
    price = [CLRV_PRICE, CLRV_PRICE, ALRV_PRICE][int(car.number) % 1000 / 100]

    #geopy is lat,lon, mongo is lon,lat
    traveled = distance(*(stop.location[::-1] for stop in (on,off))) 
    fare_paid = round(traveled.kilometers * price)

    return fare_paid

def get_streetcar_price(user, car):
    #No rules here yet
    return 200
