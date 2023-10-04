from json_parser import parse_json
from unittest import TestCase, mock

example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'


class ParserTest(TestCase):
    def test_empty_args(self):
        with self.assertRaises(TypeError) as err:
            parse_json(example, [], ['w1'])

        self.assertEqual("required_fields is None or empty", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            parse_json(example, ['k1'])

        self.assertEqual("keywords is None or empty", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            parse_json(example, [], [])

        self.assertEqual("required_fields and keywords is None or empty", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            parse_json('', ['k1', 'k4'], ['w1'])

        self.assertEqual("json_str is empty", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def test_parse_without_calls(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1'], ['w5'], mock_print)
            expected_calls = []
            self.assertEqual(expected_calls, mock_print.mock_calls)

            parse_json(example, ['k9'], ['w1', 'w2'], mock_print)
            expected_calls = []
            self.assertEqual(expected_calls, mock_print.mock_calls)

    def test_parse_leq_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['w1'], mock_print)
            expected_calls_num = 2
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k4'], ['w2', 'w4', 'w8', 'w11'], mock_print)
            expected_calls_num = 2
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

    def test_parse_geq_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2', 'k5'], ['w2'], mock_print)
            expected_calls_num = 1
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k4', 'k4', 'k8'], ['w6', 'w4', 'w8', 'w11'], mock_print)
            expected_calls_num = 3
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

    def test_parse_similar_keywords(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['w2', 'w2'], mock_print)
            expected_calls_num = 1
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k4'], ['w6', 'w4', 'w4', 'w4'], mock_print)
            expected_calls_num = 3
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

    def test_parse_similar_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2', 'k1'], ['w2'], mock_print)
            expected_calls_num = 1
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k2', 'k4', 'k4'], ['w6', 'w4'], mock_print)
            expected_calls_num = 3
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

    def test_parse_register_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'K2'], ['w1'], mock_print)
            expected_calls_num = 1
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['K2'], ['w6', 'w4'], mock_print)
            expected_calls_num = 0
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

    # '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_register_words(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['W1'], mock_print)
            expected_calls_num = 2
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k4'], ['W6', 'w4'], mock_print)
            expected_calls_num = 3
            self.assertEqual(expected_calls_num, len(mock_print.mock_calls))
