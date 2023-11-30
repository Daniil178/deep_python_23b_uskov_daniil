import json
import random
import string
from unittest import TestCase
import timeit

import ujson

import cjson


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class TestJson(TestCase):
    def setUp(self):
        self.large_data = {}
        for i in range(10000):  # Измените этот диапазон на нужный размер
            key = generate_random_string(10)
            if i % 2 == 0:
                value = generate_random_string(20)
            else:
                value = random.randint(-1000, 1000)
            self.large_data[key] = value

    def test_errors(self):
        json_list = [{"hello": 10, "world": "value"}]

        with self.assertRaises(TypeError) as err:
            cjson.loads(json_list)

        self.assertEqual("Expected a string", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            cjson.dumps()

        self.assertEqual("Expected a PyObject", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            cjson.dumps(json_list)

        self.assertEqual("Expected a dictionary", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def test_json_loads(self):
        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str)
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(json_doc, ujson_doc)
        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(json_str, cjson.dumps(cjson.loads(json_str)))

    def test_json_dumps(self):
        json_dict = {"hello": 10, "world": "value"}
        json_doc = json.dumps(json_dict)
        ujson_doc = ujson.dumps(json_dict, separators=(", ", ": "))
        cjson_doc = cjson.dumps(json_dict)

        self.assertEqual(json_doc, ujson_doc)
        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(json_dict, cjson.loads(cjson.dumps(json_dict)))

    def test_cjson_dumps(self):
        def cjson_dumps():
            cjson.dumps(self.large_data)

        cjson_time = min(timeit.repeat(cjson_dumps, number=100, repeat=5))
        print(f"cjson.dumps time: {cjson_time} seconds")

    def test_ujson_dumps(self):
        def ujson_dumps():
            ujson.dumps(self.large_data)

        ujson_time = min(timeit.repeat(ujson_dumps, number=100, repeat=5))
        print(f"ujson.dumps time: {ujson_time} seconds")

    def test_cjson_loads(self):
        cjson_string = cjson.dumps(self.large_data)

        def cjson_loads():
            cjson.loads(cjson_string)

        cjson_time = min(timeit.repeat(cjson_loads, number=100, repeat=5))
        print(f"cjson.loads time: {cjson_time} seconds")

    def test_ujson_loads(self):
        ujson_string = ujson.dumps(self.large_data)

        def ujson_loads():
            ujson.loads(ujson_string)

        ujson_time = min(timeit.repeat(ujson_loads, number=100, repeat=5))
        print(f"ujson.loads time: {ujson_time} seconds")
