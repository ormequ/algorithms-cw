import sys


class HashNode:
    def __init__(self, key, value=None):
        self.deleted = False
        self.key = key
        self.value = value

    def __eq__(self, other):
        if isinstance(other, HashNode):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, HashNode):
            return self.value < other.value
        return self.value < other

    def __str__(self):
        return f'"{self.key}": {self.value}'


class HashTable:
    def __init__(self, hash_first, hash_second, buffer=1024, rehash_size=0.8, repeat_keys=False):
        if not (0 < rehash_size <= 1):
            rehash_size = 0.8
        self.size = 0
        self.repeat_keys = repeat_keys
        self.exists_size = 0
        self.buffer = buffer
        self.data = [HashNode(None) for _ in range(self.buffer)]
        self.rehash_size = rehash_size
        self.hash_first = hash_first
        self.hash_second = hash_second

    def insert(self, key):
        self.__setitem__(key, None)

    def __setitem__(self, key, value):
        if self.exists_size + 1 > self.rehash_size * self.buffer:
            self.resize()
        if self.size > 2 * self.exists_size:
            self.rehash()
        h1 = self.hash_first(key, self.buffer)
        h2 = self.hash_second(key, self.buffer)
        first_erased = None
        for i in range(self.buffer):
            if self.data[h1].key is None:
                break
            elif self.data[h1].key == key:
                if not self.data[h1].deleted and not self.repeat_keys:
                    self.data[h1].value = value
                    return
                elif self.data[h1].deleted:
                    first_erased = h1
            h1 = (h1 + h2) % self.buffer

        if first_erased is not None:
            self.data[first_erased].deleted = False
            self.data[first_erased].value = value
        else:
            self.data[h1] = HashNode(key, value)
            self.size += 1
        self.exists_size += 1

    def resize(self):
        buffer_before = self.buffer
        self.buffer = self.buffer * 2
        self.data += [HashNode(None) for _ in range(buffer_before, self.buffer)]

    def rehash(self):
        before_data = self.data
        self.data = [HashNode(None) for _ in range(self.buffer)]
        self.size = 0
        self.exists_size = 0
        for i in range(len(before_data)):
            if before_data[i].key is not None and not before_data[i].deleted:
                self.__setitem__(before_data[i].key, before_data[i].value)

    def find(self, key):
        if key is None:
            return None
        h1 = self.hash_first(key, self.buffer)
        h2 = self.hash_second(key, self.buffer)
        for i in range(self.buffer):
            if self.data[h1].key is None:
                break
            elif self.data[h1].key == key and not self.data[h1].deleted:
                return h1
            h1 = (h1 + h2) % self.buffer
        return None

    def __getitem__(self, key):
        idx = self.find(key)
        if idx is None:
            return None
        return self.data[idx].value

    def erase(self, key):
        idx = self.find(key)
        if idx is None:
            return
        self.data[idx].deleted = True
        self.exists_size -= 1

    def __str__(self):
        res = '{'
        for i in range(self.buffer):
            if self.data[i].key is not None:
                val = "\n\t".join(str(self.data[i].value).split('\n'))
                res += f'\n\t"{self.data[i].key}": {val},\t\t[{i}]'
                if self.data[i].deleted:
                    res += "\tDELETED"
        if len(res) > 1:
            res += '\n'
        return res + '}'

    def get_size(self):
        return sys.getsizeof(self.data)
