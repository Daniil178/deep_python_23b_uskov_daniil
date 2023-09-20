import io
from unittest import TestCase, mock

from model import SomeModel, predict_message_mood
from generator import FilterFile


class ModelTest(TestCase):
    def test_model(self):
        result_something: bool = 0 < SomeModel.predict("qwe") < 1
        self.assertEqual(True, result_something)

        result_empty: bool = 0 < SomeModel.predict() < 1
        self.assertEqual(True, result_empty)

        result_false: float = SomeModel.predict("something")
        self.assertEqual(False, result_false < 0 or result_false > 1)

    def test_predict_mood(self):
        with mock.patch.object(SomeModel, "predict", return_value=0.0):
            result = predict_message_mood("qwe", SomeModel())
            self.assertEqual("неуд", result)

        with mock.patch.object(SomeModel, "predict", return_value=1.0):
            result = predict_message_mood("qwe", SomeModel())
            self.assertEqual("отл", result)

        with mock.patch.object(SomeModel, "predict", return_value=0.5):
            result = predict_message_mood("qwe", SomeModel())
            self.assertEqual("норм", result)

    def test_error_not_str_in_model(self):
        with self.assertRaises(TypeError) as err:
            SomeModel().predict(1234)

        self.assertEqual("message is not string", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def tests_errors_type_model(self):
        with self.assertRaises(TypeError) as err:
            predict_message_mood("qwe", 5)

        self.assertEqual("wrong model", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def tests_errors_thresholds(self):
        with mock.patch.object(SomeModel, "predict", return_value=0.5):
            with self.assertRaises(TypeError) as err:
                predict_message_mood("qwerty", SomeModel(), 0.5, 0.2)

            self.assertEqual("bad thresholds", str(err.exception))
            self.assertEqual(TypeError, type(err.exception))

            with self.assertRaises(TypeError) as err:
                predict_message_mood("qwerty", SomeModel(), -0.1, 0.2)

            self.assertEqual("bad thresholds", str(err.exception))
            self.assertEqual(TypeError, type(err.exception))

            with self.assertRaises(TypeError) as err:
                predict_message_mood("qwerty", SomeModel(), 0.2, 1.5)

            self.assertEqual("bad thresholds", str(err.exception))
            self.assertEqual(TypeError, type(err.exception))


class GeneratorTest(TestCase):
    def test_file_create_class(self):
        with self.assertRaises(TypeError) as err:
            FilterFile("", "qwer")

        self.assertEqual("file object is not TextIO", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with open("example.txt", "r", encoding="utf-8") as file:
            with self.assertRaises(TypeError) as err:
                FilterFile(file)

        self.assertEqual("filename is not string", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(FileNotFoundError) as err:
            FilterFile("NOT_FILE.txt")

        self.assertEqual(
            "[Errno 2] No such file or directory: 'NOT_FILE.txt'",
            str(err.exception)
                         )
        self.assertEqual(FileNotFoundError, type(err.exception))

    def test_filter_empties(self):
        # empty filter
        with open("example.txt", "r", encoding="utf-8") as file:
            gen = FilterFile("", file).filter_text([])
            with self.assertRaises(StopIteration) as err:
                next(gen)

            self.assertEqual('', str(err.exception))
            self.assertEqual(StopIteration, type(err.exception))

        # empty file
        file = io.StringIO('')
        gen = FilterFile("", file).filter_text(['qwerty'])
        with self.assertRaises(StopIteration) as err:
            next(gen)

        self.assertEqual('', str(err.exception))
        self.assertEqual(StopIteration, type(err.exception))

    def test_filter_diff_case(self):
        file = io.StringIO('QwerTY ertyq\nasdfrw qweedffg')
        gen = FilterFile("", file).filter_text(['QwerTY'])

        self.assertEqual('QwerTY ertyq\n', next(gen))
        with self.assertRaises(StopIteration) as err:
            next(gen)

        self.assertEqual('', str(err.exception))
        self.assertEqual(StopIteration, type(err.exception))

        file = io.StringIO('QwertY ertyq\narw qweedffg')
        gen = FilterFile("", file).filter_text(['qwErty'])

        self.assertEqual('QwertY ertyq\n', next(gen))
        with self.assertRaises(StopIteration) as err:
            next(gen)

        self.assertEqual('', str(err.exception))
        self.assertEqual(StopIteration, type(err.exception))

    def test_filter_exact_match(self):
        file = io.StringIO('QwerTY ertyq\nasdfrw qweedffg')
        gen = FilterFile("", file).filter_text(['Qwer'])

        with self.assertRaises(StopIteration) as err:
            next(gen)

        self.assertEqual('', str(err.exception))
        self.assertEqual(StopIteration, type(err.exception))

        file = io.StringIO('QwertY ertyq\narw qweedffg')
        gen = FilterFile("", file).filter_text(['qwErtyr'])

        with self.assertRaises(StopIteration) as err:
            next(gen)

        self.assertEqual('', str(err.exception))
        self.assertEqual(StopIteration, type(err.exception))

    def test_filter_good_work(self):
        file = io.StringIO('zxcVFD RtY qrqweqdfdbdg\n'
                           'qweasd fghrtywek rtye\n'
                           'rty\nyrty f\nrTy dfg wer\n'
                           )
        gen = FilterFile("", file).filter_text(['RTY'])

        self.assertEqual('zxcVFD RtY qrqweqdfdbdg\n', next(gen))
        self.assertEqual('rty\n', next(gen))
        self.assertEqual('rTy dfg wer\n', next(gen))

        with self.assertRaises(StopIteration) as err:
            next(gen)

        self.assertEqual('', str(err.exception))
        self.assertEqual(StopIteration, type(err.exception))
