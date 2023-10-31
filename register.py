class register(object):

    def __init__(self, name, value = 0):
        self.value = value
        self.name = name

    # For printing purposes
    def __str__(self):
        return repr(self.name)
