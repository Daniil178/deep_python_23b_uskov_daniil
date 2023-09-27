from json_parser import parse_json
from decorator_mean import mean_last_calls
from unittest import TestCase, mock
from contextlib import redirect_stdout
from time import sleep
import io

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


class DecoratorTests(TestCase):
    def test_wrong_params(self):
        with self.assertRaises(TypeError) as err:
            @mean_last_calls('error')
            def foo(): pass

        self.assertEqual("k - number of calls is not int", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def test_decorator_leq_calls(self):
        out = io.StringIO()

        @mean_last_calls(3)
        def sleeper(delay: float = 0.5): sleep(delay / 100)

        with redirect_stdout(out):
            for i in range(1, 3):
                sleeper(i)

        res = [
            'mean time for calls 1 - 1 = 0.010',
            'mean time for calls 1 - 2 = 0.015',
            ''
        ]
        self.assertEqual(res, out.getvalue().split('\n'))

    def test_decorator_equal_calls(self):
        out = io.StringIO()

        @mean_last_calls(3)
        def sleeper(delay: float = 0.5): sleep(delay / 100)
        with redirect_stdout(out):
            for i in range(1, 4):
                sleeper(i)

        res = [
            'mean time for calls 1 - 1 = 0.010',
            'mean time for calls 1 - 2 = 0.015',
            'mean time for calls 1 - 3 = 0.020',
            ''
        ]
        self.assertEqual(res, out.getvalue().split('\n'))

    def test_decorator_geq_calls(self):
        out = io.StringIO()

        @mean_last_calls(3)
        def sleeper(delay: float = 0.5): sleep(delay / 100)
        with redirect_stdout(out):
            for i in range(1, 6):
                sleeper(i)

        res = [
            'mean time for calls 1 - 1 = 0.010',
            'mean time for calls 1 - 2 = 0.015',
            'mean time for calls 1 - 3 = 0.020',
            'mean time for calls 2 - 4 = 0.030',
            'mean time for calls 3 - 5 = 0.040',
            ''
        ]
        self.assertEqual(res, out.getvalue().split('\n'))
