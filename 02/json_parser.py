import json


def print_words(word: str) -> None:
    print(f'Keyword {word} is found')


def parse_json(
        json_str: str,
        required_fields: list[str] = None,
        keywords: list[str] = None,
        keyword_callback=print
) -> None:

    if not (required_fields and keywords):
        raise TypeError("required_fields or keywords is None or empty")

    json_dict = json.loads(json_str)
    need_keys = list(filter(lambda x: x in json_dict.keys(), required_fields))

    for key in need_keys:
        for word in json_dict[key].split():
            if word in keywords:
                keyword_callback(word)
