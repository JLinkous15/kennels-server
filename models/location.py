class Location():
    """Creates an animal instance to match API"""
    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, address ):
        self.id = id
        self.name = name
        self.address = address
        self.animals = None