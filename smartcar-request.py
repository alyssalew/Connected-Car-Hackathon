import smartcar

access_token = 'b4438316-f102-4811-a915-1100ed6dcfbc'

response = smartcar.get_vehicle_ids(access_token)
vid = response['vehicles'][0]
vehicle = smartcar.Vehicle(vid, access_token)


def get_location(vehicle):
    """ get the car location"""
    location = vehicle.location()
    return location

def lock_car(vehicle):
    """" Lock the car """
    lock = vehicle.lock()
    return lock

def unlock_car(vehicle):
    """ Unlock the car """
    unlock = vehicle.unlock()
    return unlock


def get_odometer(vehicle):
    """ Get odometer reading of car """

    odometer = vehicle.odometer()
    return odometer


print get_location(vehicle)
# print lock_car(vehicle)
# print unlock_car(vehicle)
print get_odometer(vehicle)


