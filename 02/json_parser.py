import json


def print_words(word: str) -> None:
    print(f'Keyword {word} is found')


def parse_json(
        json_str: str,
        required_fields: list[str] = None,
        keywords: list[str] = None,
        keyword_callback=print
) -> None:

    if not json_str:
        raise TypeError("json_str is empty")
    if not (required_fields or keywords):
        raise TypeError("required_fields and keywords is None or empty")
    if not required_fields:
        raise TypeError("required_fields is None or empty")
    if not keywords:
        raise TypeError("keywords is None or empty")

    json_dict = json.loads(json_str)
    need_keys = list(set(filter(lambda x: x in json_dict.keys(), required_fields)))
    keywords_lower = list(map(lambda x: x.lower(), keywords))

    for key in need_keys:
        for word in json_dict[key].split():
            if word.lower() in keywords_lower:
                keyword_callback(word)
