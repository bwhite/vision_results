class MockColumnFamily(object):

    def __init__(self):
        self.db = {}

    def get(self, key):
        return self.db[key]

    def get_count(self, key):
        return len(self.db[key])

    def remove(self, key):
        del self.db[key]

    def insert(self, key, columns):
        self.db.setdefault(key, {}).update(columns)

    def add(self, key, column, value=1):
        self.db[key][column] += 1
