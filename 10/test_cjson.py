import json
import time
from unittest import TestCase

import ujson

import cjson


class TestJson(TestCase):
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
