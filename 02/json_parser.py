import json


def print_words(key: str, word: str) -> None:
    print(f'Keyword = {word} for key = {key} is found')


def parse_json(
        json_str: str,
        required_fields: list[str] = None,
        keywords: list[str] = None,
        keyword_callback=None
) -> None:

    if type(json_str) != str:
        raise TypeError("json_str is not str")

    if required_fields and keywords and keyword_callback is not None:

        if type(required_fields) != list:
            raise TypeError("required_fields is not list")
        if type(keywords) != list:
            raise TypeError("keywords is not list")

        json_dict = json.loads(json_str)
        need_keys = sorted(list(set(filter(lambda x: x in json_dict.keys(), required_fields))))
        keywords_lower = list(map(lambda x: x.lower(), keywords))

        for key in need_keys:
            for word in json_dict[key].split():
                if word.lower() in keywords_lower:
                    keyword_callback(key, word)
