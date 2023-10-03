import io
from unittest import TestCase
from contextlib import redirect_stdout

from custom_list import CustomList


list_5 = [1, 2, 3, 4, 5]
list_3 = [5, 4, 3]
list_8 = [9, 8, 7, 6, 5, 4, 3, 2]
list_5_1 = [5, 4, 3, 2, 1]


class CustomListTests(TestCase):

    def test_init(self):
        empty = []
        self.assertEqual(list, type(empty))
        self.assertEqual(list, type(list_5))

        clist = CustomList(list_5)
        self.assertEqual(CustomList, type(clist))
        self.assertEqual(list_5, clist.data)

        clist1 = CustomList(empty)
        self.assertEqual(CustomList, type(clist1))
        self.assertEqual([], clist1.data)

        self.assertEqual(CustomList, type(CustomList()))
        self.assertEqual([], CustomList().data)

    def test_len(self):
        clist_5 = CustomList(list_5)
        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(5, len(clist_5))

        clist_3 = CustomList(list_3)
        self.assertEqual(CustomList, type(clist_3))
        self.assertEqual(3, len(clist_3))

        clist_0 = CustomList()
        self.assertEqual(CustomList, type(clist_0))
        self.assertEqual(0, len(clist_0))

    def test_add_only_custom_lists(self):
        clist_0 = CustomList()
        clist_3 = CustomList(list_3)
        clist_5 = CustomList(list_5)

        self.assertEqual(CustomList, type(clist_0))
        self.assertEqual(CustomList, type(clist_3))
        self.assertEqual(CustomList, type(clist_5))

        res_1 = clist_3 + clist_0

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([5, 4, 3], res_1.data)
        self.assertEqual([5, 4, 3], clist_3.data)
        self.assertEqual([], clist_0.data)

        res_2 = clist_5 + clist_3

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([6, 6, 6, 4, 5], res_2.data)
        self.assertEqual([5, 4, 3], clist_3.data)
        self.assertEqual([1, 2, 3, 4, 5], clist_5.data)

    def test_radd_custom_list_and_list(self):
        clist_0 = CustomList()
        clist_3 = CustomList(list_3)
        empty = []

        self.assertEqual(CustomList, type(clist_0))
        self.assertEqual(CustomList, type(clist_3))

        res_1 = empty + clist_3

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([5, 4, 3], res_1.data)
        self.assertEqual([5, 4, 3], clist_3.data)
        self.assertEqual([], empty)

        res_2 = list_5 + clist_3

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([6, 6, 6, 4, 5], res_2.data)
        self.assertEqual([5, 4, 3], clist_3.data)
        self.assertEqual([1, 2, 3, 4, 5], list_5)

    def test_add_custom_list_and_list(self):
        clist_0 = CustomList()
        clist_5 = CustomList(list_5)

        self.assertEqual(CustomList, type(clist_0))
        self.assertEqual(CustomList, type(clist_5))

        res_1 = clist_0 + list_3

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([5, 4, 3], res_1.data)
        self.assertEqual([5, 4, 3], list_3)
        self.assertEqual([], clist_0.data)

        res_2 = clist_5 + list_3

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([6, 6, 6, 4, 5], res_2.data)
        self.assertEqual([5, 4, 3], list_3)
        self.assertEqual([1, 2, 3, 4, 5], clist_5.data)

    def test_sub_only_custom_lists(self):
        clist_0 = CustomList()
        clist_3 = CustomList(list_3)
        clist_5 = CustomList(list_5)

        self.assertEqual(CustomList, type(clist_0))
        self.assertEqual(CustomList, type(clist_3))
        self.assertEqual(CustomList, type(clist_5))

        res_1 = clist_0 - clist_3

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([-5, -4, -3], res_1.data)
        self.assertEqual([5, 4, 3], clist_3.data)
        self.assertEqual([], clist_0.data)

        res_2 = clist_5 - clist_3

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([-4, -2, 0, 4, 5], res_2.data)
        self.assertEqual([5, 4, 3], clist_3.data)
        self.assertEqual([1, 2, 3, 4, 5], clist_5.data)

    def test_rsub_only_custom_lists(self):
        clist_0 = CustomList()
        clist_3 = CustomList(list_3)
        clist_5 = CustomList(list_5)

        self.assertEqual(CustomList, type(clist_0))
        self.assertEqual(CustomList, type(clist_3))
        self.assertEqual(CustomList, type(clist_5))

        res_1 = clist_3 - clist_0

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([5, 4, 3], res_1.data)
        self.assertEqual([5, 4, 3], clist_3.data)
        self.assertEqual([], clist_0.data)

        res_2 = clist_3 - clist_5

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([4, 2, 0, -4, -5], res_2.data)
        self.assertEqual([5, 4, 3], clist_3.data)
        self.assertEqual([1, 2, 3, 4, 5], clist_5.data)

    def test_sub_custom_list_and_list(self):
        clist_5 = CustomList(list_5)
        self.assertEqual(CustomList, type(clist_5))

        res_1 = clist_5 - list_3

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([-4, -2, 0, 4, 5], res_1.data)
        self.assertEqual([5, 4, 3], list_3)
        self.assertEqual([1, 2, 3, 4, 5], clist_5.data)

        res_2 = clist_5 - list_8

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([-8, -6, -4, -2, 0, -4, -3, -2], res_2.data)
        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2], list_8)
        self.assertEqual([1, 2, 3, 4, 5], clist_5.data)

    def test_rsub_custom_list_and_list(self):
        clist_5 = CustomList(list_5)
        self.assertEqual(CustomList, type(clist_5))

        res_1 = list_3 - clist_5

        self.assertEqual(CustomList, type(res_1))
        self.assertEqual([4, 2, 0, -4, -5], res_1.data)
        self.assertEqual([5, 4, 3], list_3)
        self.assertEqual([1, 2, 3, 4, 5], clist_5.data)

        res_2 = list_8 - clist_5

        self.assertEqual(CustomList, type(res_2))
        self.assertEqual([8, 6, 4, 2, 0, 4, 3, 2], res_2.data)
        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2], list_8)
        self.assertEqual([1, 2, 3, 4, 5], clist_5.data)

    def test_eq(self):
        clist_5 = CustomList(list_5_1)
        clist_5_1 = CustomList(list_5)
        clist_3 = CustomList(list_3)

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(False, clist_3 == clist_5)
        self.assertEqual(False, CustomList([1, 1, 1]) == clist_3)

        self.assertEqual(True, clist_5_1 == clist_5)
        self.assertEqual(True, CustomList([12]) == clist_3)

    def test_ne(self):
        clist_5 = CustomList(list_5_1)
        clist_5_1 = CustomList(list_5)
        clist_3 = CustomList(list_3)

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(True, clist_3 != clist_5)
        self.assertEqual(True, CustomList([1, 1, 1]) != clist_3)

        self.assertEqual(False, clist_5_1 != clist_5)
        self.assertEqual(False, CustomList([12]) != clist_3)

    def test_lt(self):
        clist_5 = CustomList(list_5_1)
        clist_5_1 = CustomList(list_5)
        clist_3 = CustomList(list_3)

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(True, clist_3 < clist_5)
        self.assertEqual(True, CustomList([1, 1, 1]) < clist_3)

        self.assertEqual(False, clist_5_1 < clist_5)
        self.assertEqual(False, CustomList([12, 3]) < clist_3)

    def test_le(self):
        clist_5 = CustomList(list_5_1)
        clist_5_1 = CustomList(list_5)
        clist_3 = CustomList(list_3)

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(True, clist_3 <= clist_5)
        self.assertEqual(False, CustomList([1, 1, 1, 10]) <= clist_3)

        self.assertEqual(True, clist_5_1 <= clist_5)
        self.assertEqual(False, CustomList([12, 3]) <= clist_3)

    def test_gt(self):
        clist_5 = CustomList(list_5_1)
        clist_5_1 = CustomList(list_5)
        clist_3 = CustomList(list_3)

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(False, clist_3 > clist_5)
        self.assertEqual(False, CustomList([1, 1, 1]) > clist_3)

        self.assertEqual(False, clist_5_1 > clist_5)
        self.assertEqual(True, CustomList([12, 3]) > clist_3)

    def test_ge(self):
        clist_5 = CustomList(list_5_1)
        clist_5_1 = CustomList(list_5)
        clist_3 = CustomList(list_3)

        self.assertEqual(CustomList, type(clist_5))
        self.assertEqual(CustomList, type(clist_5_1))
        self.assertEqual(CustomList, type(clist_3))

        self.assertEqual(False, clist_3 >= clist_5)
        self.assertEqual(True, CustomList([1, 1, 1, 10]) >= clist_3)

        self.assertEqual(True, clist_5_1 >= clist_5)
        self.assertEqual(True, CustomList([12, 3]) >= clist_3)

    def test_str(self):
        out = io.StringIO()

        clist_3 = CustomList(list_3)
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
        clist_8 = CustomList(list_8)
        self.assertEqual(CustomList, type(clist_empty))
        self.assertEqual(CustomList, type(clist_8))

        res = ['|[9, 8, 7, 6, 5, 4, 3, 2], sum = 44|, |[], sum = 0|', '']
        with redirect_stdout(out):
            print(clist_8, clist_empty, sep=', ')

        self.assertEqual(res, out.getvalue().split('\n'))
