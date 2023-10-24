from collections import deque


class LRUCache:
    __slots__ = ["__values", "__limit", "__last_used"]

    def __init__(self, limit: int = 42):
        self.__limit = limit
        self.__values = {}
        self.__last_used = deque()

    def __update_deque(self, key: str) -> None:
        if key in self.__last_used:
            self.__last_used.remove(key)

        self.__last_used.append(key)
        if len(self.__last_used) > self.__limit:
            del_key = self.__last_used.popleft()
            self.__values.pop(del_key)

    def __getitem__(self, key: str):
        if key not in self.__last_used:
            return None

        value = self.__values[key]
        self.__update_deque(key)
        return value

    def __setitem__(self, key: str, value: str) -> None:
        self.__values[key] = value
        self.__update_deque(key)
