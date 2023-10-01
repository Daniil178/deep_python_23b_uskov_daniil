import io
from unittest import TestCase, mock
from generator import FilterFile


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

    def test_filter_two_filters_in_str(self):
        file = io.StringIO('zxcVFD RtY qrqweqdfdbdg\n'
                           'qweasd fghrtywek rtye\n'
                           'rty\nyrty f\nrTy dfg wer\n'
                           )
        gen = FilterFile("", file).filter_text(['RTY', 'zxcvfd', 'dfg'])

        self.assertEqual('zxcVFD RtY qrqweqdfdbdg\n', next(gen))
        self.assertEqual('rty\n', next(gen))
        self.assertEqual('rTy dfg wer\n', next(gen))

        with self.assertRaises(StopIteration) as err:
            next(gen)

        self.assertEqual('', str(err.exception))
        self.assertEqual(StopIteration, type(err.exception))

    def test_filter_filter_is_str(self):
        file = io.StringIO('zxcVFD RtY qrqweqdfdbdg\n\n'
                           'qweasd fghrtywek rtye\n'
                           'rty\nyrty f\nrTy dfg wer\n'
                           )
        gen = FilterFile("", file).filter_text(['zxcVFD RtY qrqweqdfdbdg', 'FD RtY qrqw'])

        self.assertEqual('zxcVFD RtY qrqweqdfdbdg\n', next(gen))

        with self.assertRaises(StopIteration) as err:
            next(gen)

        self.assertEqual('', str(err.exception))
        self.assertEqual(StopIteration, type(err.exception))
