class Dict:
    def __init__(self, keys):
        self.data = {k: {k2: 0 for k2 in keys if k != k2} for k in keys}

    def __setitem__(self, key, value):
        a, b = key
        self.data[a][b] = value
        self.data[b][a] = -value

    def __getitem__(self, item):
        a, b = item
        return self.data[a][b]

    def values_by(self, item):
        return self.data[item].values()

