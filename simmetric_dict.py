class SDict:
    def __init__(self):
        self.data = {}

    def _key(self, a, b):
        return ((a, b), 1) if id(a) < id(b) else ((b, a), -1)

    def __setitem__(self, key, value):
        key, m = self._key(*key)
        self.data[key] = value * m

    def get(self, a, b, default = None):
        key, m = self._key(a, b)
        return self.data.get(key, default) * m

    def values_by(self, item):
        for key in self.data.keys():
            if item in key:
                m = 1 if item == key[0] else -1
                yield self.data.get(key) * m

    def __contains__(self, item):
        return self._key(*item) in self.data

    def clean(self):
        self.data = {}
