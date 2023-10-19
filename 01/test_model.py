from unittest import TestCase, mock
from model import SomeModel, predict_message_mood


class ModelTest(TestCase):
    def test_model(self):
        param1: str = "qwe"
        param2: str = "something"

        self.assertEqual(str, type(param1))
        self.assertEqual(str, type(param2))

        result_something: bool = 0 < SomeModel.predict(param1) < 1
        self.assertEqual(True, result_something)

        result_empty: bool = 0 < SomeModel.predict() < 1
        self.assertEqual(True, result_empty)

        result_false: float = SomeModel.predict(param2)
        self.assertEqual(False, result_false < 0 or result_false > 1)

    def test_predict_mood(self):
        param1: str = "qwe"
        self.assertEqual(str, type(param1))

        model = SomeModel()
        model.predict = mock.MagicMock(return_value=0.0)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("неуд", result)

        model.predict = mock.MagicMock(return_value=1.0)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("отл", result)

        model.predict = mock.MagicMock(return_value=0.5)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("норм", result)

    def test_predict_border(self):
        param1: str = "qwe"
        self.assertEqual(str, type(param1))
        model = SomeModel()

        model.predict = mock.MagicMock(return_value=0.3)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("норм", result)

        model.predict = mock.MagicMock(return_value=0.8)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("норм", result)

        model.predict = mock.MagicMock(return_value=0.29999999)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("неуд", result)

        model.predict = mock.MagicMock(return_value=0.80000001)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("отл", result)

        model.predict = mock.MagicMock(return_value=0.301)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("норм", result)

        model.predict = mock.MagicMock(return_value=0.7999999)
        result = predict_message_mood(param1, model)
        model.predict.assert_called_with("qwe")
        self.assertEqual("норм", result)

    def test_predict_change_border(self):
        param1: str = "message"
        self.assertEqual(str, type(param1))
        model = SomeModel()

        model.predict = mock.MagicMock(return_value=0.3)
        result = predict_message_mood(param1, model, 0.4)
        model.predict.assert_called_with("message")
        self.assertEqual("неуд", result)

        model.predict = mock.MagicMock(return_value=0.8)
        result = predict_message_mood(param1, model, 0.1, 0.9)
        model.predict.assert_called_with("message")
        self.assertEqual("норм", result)

        model.predict = mock.MagicMock(return_value=0.2)
        result = predict_message_mood(param1, model, 0.1, 0.15)
        model.predict.assert_called_with("message")
        self.assertEqual("отл", result)

        model.predict = mock.MagicMock(return_value=0.9)
        result = predict_message_mood(param1, model, 0.92, 0.99)
        model.predict.assert_called_with("message")
        self.assertEqual("неуд", result)

        model.predict = mock.MagicMock(return_value=0.301)
        result = predict_message_mood(param1, model, 0.301)
        model.predict.assert_called_with("message")
        self.assertEqual("норм", result)

        model.predict = mock.MagicMock(return_value=0.79999)
        result = predict_message_mood(param1, model, 0.79, 0.799)
        model.predict.assert_called_with("message")
        self.assertEqual("отл", result)

    def test_error_not_str_in_model(self):
        param: int = 1234
        self.assertEqual(int, type(param))

        with self.assertRaises(TypeError) as err:
            SomeModel().predict(param)

        self.assertEqual("message is not string", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def tests_errors_type_model(self):
        param: str = "qwe"
        self.assertEqual(str, type(param))

        with self.assertRaises(TypeError) as err:
            predict_message_mood(param, 5)

        self.assertEqual("wrong model", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

    def tests_errors_thresholds(self):
        message: str = "qwerty"
        self.assertEqual(str, type(message))
        model = SomeModel()

        model.predict = mock.MagicMock(return_value=0.5)

        with self.assertRaises(TypeError) as err:
            predict_message_mood(message, model, 0.5, 0.2)
            model.predict.assert_called_with("qwerty")

        self.assertEqual("bad thresholds", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            predict_message_mood(message, model, -0.1, 0.2)
            model.predict.assert_called_with("qwerty")

        self.assertEqual("bad thresholds", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            predict_message_mood(message, model, 0.2, 1.5)
            model.predict.assert_called_with("qwerty")

        self.assertEqual("bad thresholds", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        with self.assertRaises(TypeError) as err:
            predict_message_mood(message, model, 0.9)
            model.predict.assert_called_with("qwerty")

        self.assertEqual("bad thresholds", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))
