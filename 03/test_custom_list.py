import io
from unittest import TestCase
from contextlib import redirect_stdout

from custom_list import CustomList


class CustomListTests(TestCase):

    def test_init(self):
        empty = []
        self.assertEqual(list, type(empty))
        self.assertEqual(list, type([1, 2, 3]))

        clist = CustomList([2, 3, 4, 5])
        self.assertEqual(CustomList, type(clist))
        self.assertEqual([2, 3, 4, 5], clist)

        clist1 = CustomList(empty)
        self.assertEqual(CustomList, type(clist1))
        self.assertEqual([], clist1)

        self.assertEqual(CustomList, type(CustomList()))
        self.assertEqual([], CustomList())

    def test_add_only_custom_lists(self):
        clist_0 = CustomList()
        clist_3 = CustomList([1, 2, 3])

        self.assertEqual(CustomList, type(clist_0))
        self.assertEqual(CustomList, type(clist_3))

        res_1 = clist_3 + clist_0

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([1, 2, 3], res_1)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([], clist_0)

        res_2 = clist_0 + clist_3

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([1, 2, 3], res_2)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([], clist_0)

        clist_3_1 = CustomList([3, 2, 1])
        res_3 = clist_3_1 + clist_3

        self.assertEqual(CustomList, type(clist_3_1))
        self.assertEqual(CustomList, type(res_3))
        self.assertEqual([4, 4, 4], res_3)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([3, 2, 1], clist_3_1)

    def test_radd_custom_list_and_list(self):
        clist_3 = CustomList([1, 2, 3])
        empty = []

        self.assertEqual(CustomList, type(clist_3))
        res_1 = empty + clist_3

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([1, 2, 3], res_1)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([], empty)

        list_5 = [1, 2, 3, 4, 5]
        res_2 = list_5 + clist_3

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([2, 4, 6, 4, 5], res_2)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([1, 2, 3, 4, 5], list_5)

        list_3 = [3, 4, 5]
        res_3 = list_3 + clist_3

        self.assertEqual(CustomList, type(res_3))
        self.assertEqual([4, 6, 8], res_3)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([3, 4, 5], list_3)

    def test_add_custom_list_and_list(self):
        clist_3 = CustomList([1, 2, 3])
        list_5 = [1, 2, 3, 4, 5]

        self.assertEqual(CustomList, type(clist_3))

        list_0 = []
        res_1 = clist_3 + list_0

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([1, 2, 3], res_1)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([], list_0)

        res_2 = clist_3 + list_5

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([2, 4, 6, 4, 5], res_2)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([1, 2, 3, 4, 5], list_5)

        list_3 = [1, 2, 5]
        res_3 = clist_3 + list_3

        self.assertEqual(CustomList, type(res_3))
        self.assertEqual([2, 4, 8], res_3)
        self.assertEqual([1, 2, 3], clist_3)
        self.assertEqual([1, 2, 5], list_3)

    def test_sub_only_custom_lists(self):
        clist_3 = CustomList([3, 4, 5])
        clist_5 = CustomList([1, 2, 3, 4, 5])

        self.assertEqual(CustomList, type(clist_3))
        self.assertEqual(CustomList, type(clist_5))

        res_1 = clist_5 - clist_3

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([-2, -2, -2, 4, 5], res_1)
        self.assertEqual([3, 4, 5], clist_3)
        self.assertEqual([1, 2, 3, 4, 5], clist_5)

        res_2 = clist_3 - clist_5

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([2, 2, 2, -4, -5], res_2)
        self.assertEqual([3, 4, 5], clist_3)
        self.assertEqual([1, 2, 3, 4, 5], clist_5)

        clist_3_1 = [1, 2, 3]
        res_3 = clist_3 - clist_3_1

        self.assertEqual(CustomList, type(res_3))
        self.assertEqual([2, 2, 2], res_3)
        self.assertEqual([3, 4, 5], clist_3)
        self.assertEqual([1, 2, 3], clist_3_1)

    def test_sub_custom_list_and_list(self):
        clist_5 = CustomList([1, 2, 3, 4, 5])
        list_3 = [2, 3, 4]
        list_6 = [3, 3, 3, 1, 2, 3]

        self.assertEqual(CustomList, type(clist_5))

        res_1 = clist_5 - list_3

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([-1, -1, -1, 4, 5], res_1)
        self.assertEqual([2, 3, 4], list_3)
        self.assertEqual([1, 2, 3, 4, 5], clist_5)

        res_2 = clist_5 - list_6

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([-2, -1, 0, 3, 3, -3], res_2)
        self.assertEqual([3, 3, 3, 1, 2, 3], list_6)
        self.assertEqual([1, 2, 3, 4, 5], clist_5)

        list_5 = [5, 4, 3, 2, 1]
        res_3 = clist_5 - list_6

        self.assertEqual(CustomList, type(res_3))
        self.assertEqual([-4, -2, 0, 2, 4], res_3)
        self.assertEqual([5, 4, 3, 2, 1], list_5)
        self.assertEqual([1, 2, 3, 4, 5], clist_5)

    def test_rsub_custom_list_and_list(self):
        clist_5 = CustomList([1, 2, 3, 4, 5])
        list_3 = [2, 3, 4]
        list_6 = [3, 3, 3, 1, 2, 3]

        self.assertEqual(CustomList, type(clist_5))

        res_1 = list_3 - clist_5

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([1, 1, 1, -4, -5], res_1)
        self.assertEqual([2, 3, 4], list_3)
        self.assertEqual([1, 2, 3, 4, 5], clist_5)

        res_2 = list_6 - clist_5

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([2, 1, 0, -3, -3, 3], res_2)
        self.assertEqual([3, 3, 3, 1, 2, 3], list_6)
        self.assertEqual([1, 2, 3, 4, 5], clist_5)

        list_5 = [8, 7, 6, 5, 4]
        res_3 = list_5 - clist_5

        self.assertEqual(CustomList, type(res_3))
        self.assertEqual([7, 5, 3, 1, -1], res_3)
        self.assertEqual([8, 7, 6, 5, 4], list_5)
        self.assertEqual([1, 2, 3, 4, 5], clist_5)

    def test_eq(self):
        clist_5 = CustomList([1, 2, 3, 4, 5])
        clist_5_1 = CustomList([2, 3, 4, 5, 1])
        clist_3 = CustomList([1, 2, 3])

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(False, clist_3 == clist_5)
        self.assertEqual(False, CustomList([1, 1, 1]) == clist_3)

        self.assertEqual(True, clist_5_1 == clist_5)
        self.assertEqual(True, CustomList([6]) == clist_3)

    def test_ne(self):
        clist_5 = CustomList([1, 2, 3, 4, 10])
        clist_5_1 = CustomList([2, 3, 4, 5, 6])
        clist_3 = CustomList([2, 3, 4])

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(True, clist_3 != clist_5)
        self.assertEqual(True, CustomList([1, 1, 1]) != clist_3)

        self.assertEqual(False, clist_5_1 != clist_5)
        self.assertEqual(False, CustomList([9]) != clist_3)

    def test_lt(self):
        clist_5 = CustomList([1, 2, 3, 4, 10])
        clist_5_1 = CustomList([2, 3, 4, 5, 6])
        clist_3 = CustomList([2, 3, 4])

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(True, clist_3 < clist_5)
        self.assertEqual(True, CustomList([1, 1, 1]) < clist_3)

        self.assertEqual(False, clist_5_1 < clist_5)
        self.assertEqual(False, CustomList([12]) < clist_3)

    def test_le(self):
        clist_5 = CustomList([1, 2, 3, 4, 10])
        clist_5_1 = CustomList([2, 3, 4, 5, 6])
        clist_3 = CustomList([2, 3, 4])

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(True, clist_3 <= clist_5)
        self.assertEqual(True, CustomList([1, 1, 1]) <= clist_3)

        self.assertEqual(True, clist_5_1 <= clist_5)
        self.assertEqual(False, CustomList([12]) <= clist_3)

    def test_gt(self):
        clist_5 = CustomList([1, 2, 3, 4, 10])
        clist_5_1 = CustomList([2, 3, 4, 5, 6])
        clist_3 = CustomList([2, 3, 4])

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(True, clist_5 > clist_3)
        self.assertEqual(True, CustomList([1, 1, 12]) > clist_3)

        self.assertEqual(False, clist_5_1 > clist_5)
        self.assertEqual(False, CustomList([2]) > clist_3)

    def test_ge(self):
        clist_5 = CustomList([1, 2, 3, 4, 10])
        clist_5_1 = CustomList([2, 3, 4, 5, 6])
        clist_3 = CustomList([2, 3, 4])

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(True, clist_5 >= clist_3)
        self.assertEqual(False, CustomList([1, 1, 1]) >= clist_3)

        self.assertEqual(True, clist_5_1 >= clist_5)
        self.assertEqual(False, CustomList([1]) >= clist_3)

    def test_str(self):
        out = io.StringIO()

        clist_3 = CustomList([5, 4, 3])
        self.assertEqual(CustomList, type(clist_3))

        res = ['|[5, 4, 3], sum = 12|', '']
        with redirect_stdout(out):
            print(clist_3)

        self.assertEqual(res, out.getvalue().split('\n'))

        out = io.StringIO()

        clist_empty = CustomList()
        self.assertEqual(CustomList, type(clist_empty))

        res = ['|[], sum = 0|', '']
        with redirect_stdout(out):
            print(clist_empty)

        self.assertEqual(res, out.getvalue().split('\n'))

    def test_str_with_many_custom_lists(self):
        out = io.StringIO()

        clist_empty = CustomList()
        clist_8 = CustomList([9, 8, 7, 6, 5, 4, 3, 2])
        self.assertEqual(CustomList, type(clist_empty))
        self.assertEqual(CustomList, type(clist_8))

        res = ['|[9, 8, 7, 6, 5, 4, 3, 2], sum = 44|, |[], sum = 0|', '']
        with redirect_stdout(out):
            print(clist_8, clist_empty, sep=', ')

        self.assertEqual(res, out.getvalue().split('\n'))
