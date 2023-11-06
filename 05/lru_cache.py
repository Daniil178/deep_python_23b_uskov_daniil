from typing import Any


class LRUCache:
    __slots__ = ["__dict", "__limit", "__first_elem", "__last_elem"]

    def __init__(self, limit: int = 42):
        self.__limit = limit
        self.__dict: dict[str, tuple[Any, str, str]] = {}
        # key: (value, prev, next)
        self.__first_elem: str
        self.__last_elem: str

    def __update_dict(self, key: str) -> None:
        value = self.__dict[key][0]
        if key in self.__dict:
            self.__remove_from_dict(key)

        self[key] = value

    def __remove_from_dict(self, key):
        prev_elem = self.__dict[key][1]
        next_elem = self.__dict[key][2]
        if prev_elem:
            self.__dict[prev_elem] = (
                self.__dict[prev_elem][0],
                self.__dict[prev_elem][1],
                next_elem,
            )
        else:
            self.__first_elem = next_elem
        if next_elem:
            self.__dict[next_elem] = (
                self.__dict[next_elem][0],
                prev_elem,
                self.__dict[next_elem][2],
            )
        else:
            self.__last_elem = prev_elem

        del self.__dict[key]

    def __getitem__(self, key: str):
        if key not in self.__dict:
            return None

        value = self.__dict[key][0]
        self.__update_dict(key)
        return value

    def __setitem__(self, key: str, value: str) -> None:
        if not self.__dict.keys():
            self.__dict[key] = (value, "", "")
            self.__first_elem = key
            self.__last_elem = key
        else:
            if key in self.__dict:
                self.__remove_from_dict(key)

            self.__dict[self.__last_elem] = (
                self.__dict[self.__last_elem][0],
                self.__dict[self.__last_elem][1],
                key,
            )

            self.__dict[key] = (value, self.__last_elem, "")
            self.__last_elem = key
            if self.__limit < len(self.__dict.keys()):
                self.__remove_from_dict(self.__first_elem)
