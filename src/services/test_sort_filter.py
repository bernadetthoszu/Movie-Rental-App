import unittest
from sort_filter import Sort, Filter, IterableDictionary

class TestSort(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.iter_dict = IterableDictionary()
        self.sorter = Sort()

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def test_sort_by_value(self):
        self.iter_dict.add(0, 9)
        self.iter_dict.add(1, 8)
        self.iter_dict.add(2, 3)
        self.iter_dict.add(3, 7)
        self.iter_dict.add(4, 5)
        self.iter_dict.add(5, 6)
        self.iter_dict.add(6, 4)
        self.iter_dict.add(7, 1)
        sorted_data = self.iter_dict.shellSort(lambda x, y: x < y, self.iter_dict)
        expected = IterableDictionary()
        expected.add(7, 1)
        expected.add(2, 3)
        expected.add(6, 4)
        expected.add(4, 5)
        expected.add(5, 6)
        expected.add(3, 7)
        expected.add(1, 8)
        expected.add(0, 9)

        self.assertEqual(sorted_data, expected)

    def test_sort_by_field(self):
        class Holidays:
            def __init__(self, name, month):
                self.__name = name
                self.__month = month

            def get_month(self):
                return self.__month

        c = Holidays('Christmas', 12)
        e = Holidays('Easter', 4)
        t = Holidays('Thanksgiving', 11)

        self.iter_dict.add(1, c)
        self.iter_dict.add(2, e)
        self.iter_dict.add(3, t)
        sorted_data = self.iter_dict.shellSort(lambda x, y: x.get_month() < y.get_month(), self.iter_dict)

        expected = IterableDictionary()
        expected.add(2, e)
        expected.add(3, t)
        expected.add(1, c)

        self.assertEqual(sorted_data, expected)

        other_1 = IterableDictionary()
        other_1.add(2, e)
        other_1.add(1, c)

        self.assertNotEqual(sorted_data, other_1)

        other_2 = IterableDictionary()
        other_2.add(1, e)
        other_2.add(2, t)
        other_2.add(3, c)

        self.assertNotEqual(sorted_data, other_2)

class TestFilter(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.iter_dict = IterableDictionary()
        self.filter = Filter()

    def test_filter_by_value(self):
        self.iter_dict.add(1, 'Christmas')
        self.iter_dict.add(2, 'Easter')
        self.iter_dict.add(3, 'Thanksgiving')
        iter_dict_other = IterableDictionary()
        iter_dict_other.add(1, 'Christmas')
        iter_dict_filtered = self.filter.filter(lambda x : x == 'Christmas', self.iter_dict)
        self.assertEqual(iter_dict_filtered, iter_dict_other)

    def test_filter_by_field(self):
        class Holidays:
            def __init__(self, id, name):
                self.__id = id
                self.__name = name

            def get_name(self):
                return self.__name

        c = Holidays(1, 'Christmas')
        e = Holidays(2, 'Easter')
        t = Holidays(3, 'Thanksgiving')

        self.iter_dict.add(1, c)
        self.iter_dict.add(2, e)
        self.iter_dict.add(3, t)

        iter_dict_other = IterableDictionary()
        iter_dict_other.add(1, c)
        iter_dict_filtered = self.filter.filter(lambda x: x.get_name() == 'Christmas', self.iter_dict)
        self.assertEqual(iter_dict_filtered, iter_dict_other)


class TestIterableDisctionary(unittest.TestCase):
    def setUp(self) -> None:
        unittest.TestCase.setUp(self)
        self.iter_dict = IterableDictionary()
        self.iter_dict.add(1, 'Christmas')
        self.iter_dict.add(2, 'Easter')
        self.iter_dict.add(3, 'Thanksgiving')

    def tearDown(self) -> None:
        unittest.TestCase.tearDown(self)

    def test_getters_and_setters(self):
        self.assertEqual(self.iter_dict.__getitem__(1), 'Christmas')
        self.iter_dict.__setitem__(3, 'St Patricks Day')
        self.assertEqual(self.iter_dict.__getitem__(3), 'St Patricks Day')
        self.iter_dict[3] = 'Thanksgiving'
        self.assertEqual(self.iter_dict[3], 'Thanksgiving')
        #self.assertEqual(self.iter_dict.__getitem__(3), self.iter_dict[3])
        self.assertRaisesRegex(ValueError, 'Inexistent entity!', self.iter_dict.__getitem__, 4)
        self.assertRaisesRegex(ValueError, 'Inexistent entity!', self.iter_dict.__setitem__, 4, 'Thanksgiving')

    def test_object_operations(self):
        self.assertEqual(len(self.iter_dict), 3)
        self.assertRaisesRegex(ValueError, 'Existing entity!', self.iter_dict.add, 3, 'Thanksgiving')
        del self.iter_dict[3]
        self.assertEqual(len(self.iter_dict), 2)
