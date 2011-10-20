def find_fare(user, car, on, off):
    if car.owner == user.get_profile():
        return 0
    
    #simple rules - CLRVs half as much and ALRVs
    CLRV_PRICE = 2
    ALRV_PRICE = 4
    
    #CLRVs are 40,41, ALRVs are 42
    price = [CLRV_PRICE, CLRV_PRICE, ALRV_PRICE][int(car.number) % 1000 / 100]

    traveled = on.distance_to(off)
    fare_paid = round(traveled * price)

    return fare_paid

def get_streetcar_price(user, car):
    #No rules here yet
    return 200


def can_buy_car(user, car):
    return car.owner is None
