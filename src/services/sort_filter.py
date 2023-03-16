class Sort:

    @staticmethod
    def shellSort(function, sequence):
        # {key1: val1, key2: val2, ...} = > [(key1, val1), (key2, val2), ...]
        iter_seq = iter(sequence)
        array = list()
        i = 0
        while True:
            try:
                key = next(iter_seq)
                value = sequence[key]
                array.append((key, value))
                i += 1
            except StopIteration:
                break

        n = len(array)
        interval = n // 2
        while interval > 0:
            for i in range(interval, n):
                aux = array[i]
                j = i
                while j >= interval and function(array[j - interval][1], aux[1]) is not True:
                    array[j] = array[j-interval]
                    j -= interval
                array[j] = aux
            interval //= 2

        #reconstitute sequence
        # [(key1, val1), (key2, val2), ...] => {key1 : val1, key2 : val2, ...}
        sequence = IterableDictionary()
        for l in array:
            sequence.add(l[0], l[1])
        return sequence


class Filter:

    @staticmethod
    def filter(function, sequence):
        filtered = IterableDictionary()
        iter_sequence = iter(sequence)
        while True:
            try:
                key = next(iter_sequence)
                value = sequence[key]
                if function(value) is True:
                    filtered.add(key, value)
            except StopIteration:
                break

        # for key in s:
        #     if f(s[key]) is True:
        #         filtered[key] = s[key]

        return filtered


class IterableDictionary(Filter, Sort):

    class Iterator():
        def __init__(self, col, keys):
            self._collection = col
            self._collection_keys = keys
            self._index = 0
            self._end = len(keys) - 1

        def __next__(self):
            if self._index > self._end:
                raise StopIteration
            else:
                next_key = self._collection_keys[self._index]
                self._index += 1
                return next_key

    def __init__(self):
        self._data = {}

    def add(self, key, value):
        if key in self._data:
            raise ValueError("Existing entity!")
        self._data.update({key : value})

    def clear(self):
        self._data = {}

    def __iter__(self):
        keys = list(self._data.keys())
        return self.Iterator(self, keys)

    def __getitem__(self, key):
        """"
        Returns a tuple - (key, value)!
        """
        if key not in self._data:
            raise ValueError('Inexistent entity!')
        return self._data[key]

    def __setitem__(self, key, value):
        if key not in self._data:
            raise ValueError('Inexistent entity!')
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        keys = list(self._data.keys())
        values = list(self._data.values())
        keys_other = list(other._data.keys())
        values_other = list(other._data.values())
        if len(keys) != len(keys_other):
            return False
        n = len(keys)
        for i in range(0, n):
            if keys[i] != keys_other[i] or values[i] != values_other[i]:
                return False
        return True
