class FilterModel(object):
    def __init__(self, key, operator, value):
        if not isinstance(key, basestring):
            raise TypeError("Key must be a string.")

        if not isinstance(operator, basestring):
            raise TypeError("Operator must be a string.")

        self.key = key
        self.operator = operator
        self.value = value