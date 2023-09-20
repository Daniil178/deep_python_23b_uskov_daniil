from random import random


class SomeModel:
    @staticmethod
    def predict(message: str = "") -> float:
        if not isinstance(message, str):
            raise TypeError('message is not string')
        return random()


def predict_message_mood(
        message: str,
        model: SomeModel,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:

    if (bad_thresholds > good_thresholds or
            bad_thresholds < 0 or good_thresholds > 1):
        raise TypeError("bad thresholds")

    if not isinstance(model, SomeModel):
        raise TypeError("wrong model")

    result_predict: float = model.predict(message)

    if result_predict < bad_thresholds:
        return "неуд"
    if result_predict > good_thresholds:
        return "отл"

    return "норм"
