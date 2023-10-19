from unittest import TestCase
from custom_meta import CustomMeta


class CustomClass(metaclass=CustomMeta):
    _par_prot = 10
    __par_private = 100

    def __init__(self, val):
        self.par_pub = val

    def __str__(self):
        return "Custom_by_metaclass"

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
    def test_attr(self):
        c = CustomClass(50)

        self.assertEqual(50, c.custom_par_pub)

        with self.assertRaises(AttributeError) as err:
            var = c.par_pub

        self.assertEqual("'CustomClass' object has no attribute 'par_pub'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c.custom_par_pub = 100
        self.assertEqual(100, c.custom_par_pub)

        c.par_pub = 200
        self.assertEqual(100, c.custom_par_pub)

    def test_func_public(self):
        c = CustomClass(50)

        self.assertEqual(1, c.custom_foo())
        with self.assertRaises(AttributeError) as err:
            c.foo()

        self.assertEqual("'CustomClass' object has no attribute 'foo'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c.custom_foo = lambda x: x * 2
        self.assertEqual(4, c.custom_foo(2))

    def test_func_protected(self):
        c = CustomClass(5)

        self.assertEqual(2, c._custom_boo())
        with self.assertRaises(AttributeError) as err:
            var = c._boo()

        self.assertEqual("'CustomClass' object has no attribute '_boo'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c._custom_boo = lambda x: x ** 2
        self.assertEqual(1024, c._custom_boo(32))

    def test_func_private(self):
        c = CustomClass(7)

        self.assertEqual(3, c._CustomClass__custom_go())
        with self.assertRaises(AttributeError) as err:
            var = c._CustomClass__go()

        self.assertEqual("'CustomClass' object has no attribute "
                         "'_CustomClass__go'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c._CustomClass__custom_go = lambda x: 15
        self.assertEqual(15, c._CustomClass__custom_go(4))

    def test_func_magic(self):
        c = CustomClass(10)

        self.assertEqual("Custom_by_metaclass", str(c))
        self.assertEqual(10, len(c))

    def test_add_param(self):
        c = CustomClass(50)

        c.qwe = "qwerty"
        self.assertEqual("qwerty", c.custom_qwe)
        with self.assertRaises(AttributeError) as err:
            self.assertEqual("qwerty", c.qwe)

        self.assertEqual("'CustomClass' object has no attribute 'qwe'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c._qwe = "qwerty"
        self.assertEqual("qwerty", c._custom_qwe)
        with self.assertRaises(AttributeError) as err:
            self.assertEqual("qwerty", c._qwe)

        self.assertEqual("'CustomClass' object has no attribute '_qwe'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c.__qwe = "qwerty"
        self.assertEqual("qwerty", c.__custom_qwe)
        with self.assertRaises(AttributeError) as err:
            self.assertEqual("qwerty", c._CustomClass__qwe)

        self.assertEqual("'CustomClass' object has no attribute "
                         "'_CustomClass__qwe'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

    def test_attr_class_protected(self):
        c = CustomClass(30)

        self.assertEqual(10, c._custom_par_prot)
        with self.assertRaises(AttributeError) as err:
            var = c._par_prot

        self.assertEqual("'CustomClass' object has no attribute '_par_prot'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c._custom_par_prot = 99
        self.assertEqual(99, c._custom_par_prot)
        c._par_prot = 199
        with self.assertRaises(AttributeError) as err:
            self.assertEqual(199, c._par_prot)

        self.assertEqual("'CustomClass' object has no attribute '_par_prot'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))
        self.assertEqual(99, c._custom_par_prot)

    def test_attr_class_private(self):
        c = CustomClass(4)

        self.assertEqual(100, c._CustomClass__custom_par_private)
        with self.assertRaises(AttributeError) as err:
            var = c._CustomClass__par_private

        self.assertEqual("'CustomClass' object has no attribute "
                         "'_CustomClass__par_private'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        c._CustomClass__custom_par_private = 44
        self.assertEqual(44, c._CustomClass__custom_par_private)
        c._CustomClass__par_private = 244
        with self.assertRaises(AttributeError) as err:
            self.assertEqual(244, c._CustomClass__par_private)

        self.assertEqual("'CustomClass' object has no attribute "
                         "'_CustomClass__par_private'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))
        self.assertEqual(44, c._CustomClass__custom_par_private)

    def test_class_without_exemplar(self):
        self.assertEqual(1, CustomClass.custom_foo())
        with self.assertRaises(AttributeError) as err:
            CustomClass.foo()

        self.assertEqual("type object 'CustomClass' "
                         "has no attribute 'foo'",
                         str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        CustomClass.qwe = "qwerty"
        self.assertEqual("qwerty", CustomClass.custom_qwe)
        with self.assertRaises(AttributeError) as err:
            var = CustomClass.qwe
        
        self.assertEqual("type object 'CustomClass' "
                         "has no attribute 'qwe'", str(err.exception))
        self.assertEqual(AttributeError, type(err.exception))

        CustomClass.qwe = 10
        with self.assertRaises(AttributeError) as err:
            self.assertEqual(10, CustomClass.qwe)

        self.assertEqual(
            "type object 'CustomClass' " "has no attribute 'qwe'", str(err.exception)
        )
        self.assertEqual(AttributeError, type(err.exception))
        self.assertEqual("qwerty", CustomClass.custom_qwe)

        self.assertEqual(10, CustomClass._custom_par_prot)
        with self.assertRaises(AttributeError) as err:
            var = CustomClass._par_prot
        
        self.assertEqual(
            "type object 'CustomClass' "
            "has no attribute '_par_prot'", str(err.exception)
        )
        self.assertEqual(AttributeError, type(err.exception))
        self.assertEqual(10, CustomClass._custom_par_prot)
