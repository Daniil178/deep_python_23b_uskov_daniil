from decorator_mean import mean_last_calls
from unittest import TestCase, mock
from contextlib import redirect_stdout
from time import sleep
import io


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
