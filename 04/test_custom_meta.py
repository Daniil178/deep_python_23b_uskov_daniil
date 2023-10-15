from unittest import TestCase
from custom_meta import CustomMeta


class CustomClass(metaclass=CustomMeta):
    _par_prot = 10
    __par_private = 100

    def __init__(self, val):
        self.par_pub = val

    def __len__(self):
        return self.custom_par_pub

    @staticmethod
    def foo():
        return 1

    @staticmethod
    def _boo():
        return 2

    @staticmethod
    def __go():
        return 3


class TestCustomMeta(TestCase):
    def test_new_param(self):
        c = CustomClass(50)

        self.assertEqual(50, c.custom_par_pub)

        with self.assertRaises(AttributeError) as err:
            var = c.par_pub

        self.assertEqual("'CustomClass' object has no attribute 'par_pub'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(10, c._custom_par_prot)

        with self.assertRaises(AttributeError) as err:
            var = c._par_prot

        self.assertEqual("'CustomClass' object has no attribute '_par_prot'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(100, c._CustomClass__custom_par_private)

        with self.assertRaises(AttributeError) as err:
            var = c._CustomClass__par_private

        self.assertEqual("'CustomClass' object has no attribute "
                         "'_CustomClass__par_private'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

    def test_new_func(self):
        c = CustomClass(50)

        self.assertEqual(1, c.custom_foo())

        with self.assertRaises(AttributeError) as err:
            c.foo()

        self.assertEqual("'CustomClass' object has no attribute 'foo'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(2, c._custom_boo())

        with self.assertRaises(AttributeError) as err:
            var = c._boo()

        self.assertEqual("'CustomClass' object has no attribute '_boo'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        self.assertEqual(3, c._CustomClass__custom_go())

        with self.assertRaises(AttributeError) as err:
            var = c._CustomClass__go()

        self.assertEqual("'CustomClass' object has no attribute "
                         "'_CustomClass__go'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        # magic methods don`t change name
        self.assertEqual(c.custom_par_pub, len(c))

    def test_add_param(self):
        c = CustomClass(50)

        c.qwe = "qwerty"
        self.assertEqual("qwerty", c.custom_qwe)
        with self.assertRaises(AttributeError) as err:
            var = c.qwe

        self.assertEqual("'CustomClass' object has no attribute 'qwe'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c._qwe = "qwerty"
        self.assertEqual("qwerty", c._custom_qwe)
        with self.assertRaises(AttributeError) as err:
            var = c._qwe

        self.assertEqual("'CustomClass' object has no attribute '_qwe'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c.__qwe = "qwerty"
        self.assertEqual("qwerty", c.__custom_qwe)
        with self.assertRaises(AttributeError) as err:
            var = c.__qwe

        self.assertEqual("'CustomClass' object has no attribute "
                         "'_TestCustomMeta__qwe'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))
