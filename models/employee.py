class Employee():
    """Creates an animal instance to match API"""
    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, address, location_id, location):
        self.id = id
        self.name = name
        self.address = address
        self.location_id = location_id
        location = None