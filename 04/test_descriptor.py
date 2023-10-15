from unittest import TestCase

from descriptor import StrTemplate, FixNumber, ChoiceList


class PersonStr:
    phone_number = (
        StrTemplate("\\+[1-9] [1-9][0-9]{2} [0-9]{3} [0-9]{2}-[0-9]{2}"))
    name = StrTemplate("[a-zA-Z]+")

    def __init__(self, name: str, phone_number: str):
        self.name = name
        self.phone_number = phone_number


class PersonNum:
    age = FixNumber(1, 150)
    height = FixNumber(40, 250)

    def __init__(self, age: int, height):
        self.age = age
        self.height = height


class PersonChoiceList:
    gender = ChoiceList(['Male', 'Female'])
    status = ChoiceList(['student', 'teacher', 'rector'])

    def __init__(self, gender, status):
        self.gender = gender
        self.status = status


class TestDescriptor(TestCase):

    def test_descriptor_str(self):
        p = PersonStr('Nik', '+7 123 000 12-12')

        self.assertEqual('Nik', p.name)
        self.assertEqual('+7 123 000 12-12', p.phone_number)

        with self.assertRaises(ValueError) as err:
            p.name = "Valentin2020"

        self.assertEqual("value don't equal of template", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            p.phone_number = "8 123 345 33-33"

        self.assertEqual("value don't equal of template", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            p.name = 123

        self.assertEqual("str required", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        p.name = "Daniil"
        p.phone_number = "+7 919 123 44-44"

        self.assertEqual('Daniil', p.name)
        self.assertEqual('+7 919 123 44-44', p.phone_number)

    def test_descriptor_num(self):
        p1 = PersonNum(21, 175)

        self.assertEqual(21, p1.age)
        self.assertEqual(175, p1.height)

        with self.assertRaises(ValueError) as err:
            p1.age = -5

        self.assertEqual("value don't equal of template", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            p1.height = 1343

        self.assertEqual("value don't equal of template", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            p1.age = "qwerty"

        self.assertEqual("float or int required", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        p1.age = 30
        p1.height = 205.7

        self.assertEqual(30, p1.age)
        self.assertEqual(205.7, p1.height)

    def test_descriptor_choice_list(self):
        p2 = PersonChoiceList('Male', 'student')

        self.assertEqual('Male', p2.gender)
        self.assertEqual('student', p2.status)

        with self.assertRaises(ValueError) as err:
            p2.gender = "male"

        self.assertEqual("value should in choice list", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            p2.status = "Analytic"

        self.assertEqual("value should in choice list", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            p2.status = 123

        self.assertEqual("str required", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        p2.gender = "Female"
        p2.status = "rector"

        self.assertEqual('Female', p2.gender)
        self.assertEqual('rector', p2.status)

    def test_descriptor_init_error(self):
        with self.assertRaises(TypeError) as err:
            StrTemplate(123)

        self.assertEqual("str required for template", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            FixNumber("123", 44)

        self.assertEqual("borders is float or int number", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            FixNumber(123, "123")

        self.assertEqual("borders is float or int number", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            ChoiceList(123532)

        self.assertEqual("choice list is list", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))
