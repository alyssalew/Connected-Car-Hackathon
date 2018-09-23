import smartcar

access_token = '2e19892d-fb31-4dfe-8980-b7da1b2b47a0'

response = smartcar.get_vehicle_ids(access_token)
vid = response['vehicles'][0]
vehicle = smartcar.Vehicle(vid, access_token)


def get_vehicle_info(vehicle):
    """Get the info vehicle"""
    info = vehicle.info()
    return info

def get_location(vehicle):
    """ Get the car location"""
    location = vehicle.location()
    return location

def lock_car(vehicle):
    """" Lock the car """

    return vehicle.lock()

def unlock_car(vehicle):
    """ Unlock the car """
    return vehicle.unlock()


def get_odometer(vehicle):
    """ Get odometer reading of car """

    odometer = vehicle.odometer()
    return odometer


def get_coordiates(location):
    """ Gets the coordiates of the car """

    coordiates = (location['data']['latitude'], location['data']['longitude'])
    # coordiates = location['data']
    return coordiates


# print get_vehicle_info(vehicle)
print get_location(vehicle)
# print lock_car(vehicle)
# print unlock_car(vehicle)
# print get_odometer(vehicle)
location = get_location(vehicle)
print get_coordiates(location)
