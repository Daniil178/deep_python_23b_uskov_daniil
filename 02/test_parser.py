from json_parser import parse_json
from unittest import TestCase, mock
from contextlib import redirect_stdout
import io

example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'


class ParserTest(TestCase):
    def test_empty_args(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, None, ['w5'], mock_print)
            expected_calls = []
            self.assertEqual(expected_calls, mock_print.mock_calls)

            parse_json(example, ['k1'], None, mock_print)
            expected_calls = []
            self.assertEqual(expected_calls, mock_print.mock_calls)

            parse_json(example, [], ['w1'], mock_print)
            expected_calls = []
            self.assertEqual(expected_calls, mock_print.mock_calls)

            parse_json(example, ['k1'], [], mock_print)
            expected_calls = []
            self.assertEqual(expected_calls, mock_print.mock_calls)

        out = io.StringIO()
        with redirect_stdout(out):
            parse_json(example, ['k1'], ['w1'])

        res = ['']
        self.assertEqual(res, out.getvalue().split('\n'))

    def test_wrong_type(self):
        with self.assertRaises(TypeError) as err:
            parse_json(example, 'sdrg', ['d'], print)

        self.assertEqual("required_fields is not list", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            parse_json(example, ['k'], 2, print)

        self.assertEqual("keywords is not list", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            parse_json(123)

        self.assertEqual("json_str is not str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_without_calls(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1'], ['w5'], mock_print)
            expected_calls = []
            self.assertEqual(expected_calls, mock_print.mock_calls)

            parse_json(example, ['k9'], ['w1', 'w2'], mock_print)
            expected_calls = []
            self.assertEqual(expected_calls, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_leq_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['w1'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w1'),
                mock.call('k2', 'w1')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k4'], ['w2', 'w4', 'w8', 'w11'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w2'),
                mock.call('k4', 'w4')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_geq_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2', 'k5'], ['w2'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w2')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k4', 'k4', 'k8'], ['w6', 'w4', 'w8', 'w11'], mock_print)
            expected_calls_num = [
                mock.call('k2', 'w4'),
                mock.call('k4', 'w4'),
                mock.call('k4', 'w6')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_similar_keywords(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['w2', 'w2'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w2')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k4'], ['w6', 'w4', 'w4', 'w4'], mock_print)
            expected_calls_num = [
                mock.call('k2', 'w4'),
                mock.call('k4', 'w4'),
                mock.call('k4', 'w6')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_similar_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2', 'k1'], ['w2'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w2')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k2', 'k4', 'k4'], ['w6', 'w4'], mock_print)
            expected_calls_num = [
                mock.call('k2', 'w4'),
                mock.call('k4', 'w4'),
                mock.call('k4', 'w6')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_register_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'K2'], ['w1'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w1')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['K2'], ['w6', 'w4'], mock_print)
            expected_calls_num = []
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_register_words(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['W1'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w1'),
                mock.call('k2', 'w1')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k4'], ['W6', 'w4'], mock_print)
            expected_calls_num = [
                mock.call('k2', 'w4'),
                mock.call('k4', 'w4'),
                mock.call('k4', 'w6')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_parse_exact_occurrence(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['1'], mock_print)
            expected_calls_num = []
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k2', 'k4'], ['W', 'w4'], mock_print)
            expected_calls_num = [
                mock.call('k2', 'w4'),
                mock.call('k4', 'w4')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_keywords_not_in_keys(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['w10', '12342', 'wfdggfd'], mock_print)
            expected_calls_num = []
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2', 'k4'], ['w10', 'HTTP', 'RTF', 'FTP'], mock_print)
            expected_calls_num = []
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

# example = '{"k1": "w1 w2", "k2": "w1 w4", "k4": "w4 w6"}'
    def test_many_keywords_in_str(self):
        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['w1', 'w2', 'w1', 'w2'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w1'),
                mock.call('k1', 'w2'),
                mock.call('k2', 'w1')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)

        with mock.patch("json_parser.print_words") as mock_print:
            parse_json(example, ['k1', 'k2'], ['w1', 'w2', 'w1', 'w2', 'w4', 'W4'], mock_print)
            expected_calls_num = [
                mock.call('k1', 'w1'),
                mock.call('k1', 'w2'),
                mock.call('k2', 'w1'),
                mock.call('k2', 'w4')
            ]
            self.assertEqual(expected_calls_num, mock_print.mock_calls)
