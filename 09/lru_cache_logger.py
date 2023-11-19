from typing import Any
import logging

import argparse


class CacheFilter(logging.Filter):
    def filter(self, record):
        even_words = len(record.msg.split()) % 2 == 0
        contains_set = "set" in record.msg

        return even_words and contains_set


class LRUCache:
    __slots__ = ["__dict", "__limit", "__first_elem", "__last_elem", "_logger"]

    def __init__(
        self, limit: int = 42, enable_stdout: bool = False, enable_filter: bool = False
    ) -> None:
        self.__limit = limit
        self.__dict: dict[str, tuple[Any, str, str]] = {}
        # key: (value, prev, next)
        self.__first_elem: str
        self.__last_elem: str
        self._logger = self._create_logger(enable_stdout, enable_filter)

        self._logger.debug("cache is create with limit=%s", self.__limit)

    def __update_dict(self, key: str) -> None:
        self._logger.debug("start update dict for key = `%s`", key)

        value = self.__dict[key][0]
        if key in self.__dict:
            self._logger.warning(
                "begin remove key = `%s`, val = `%s` from cache", key, value
            )
            self.__remove_from_dict(key)
            self._logger.debug("remove key = `%s` is successfully", key)

        self[key] = value

    def __remove_from_dict(self, key: str) -> None:
        self._logger.debug("start delete key=`%s` from dict", key)
        prev_elem = self.__dict[key][1]
        next_elem = self.__dict[key][2]
        if prev_elem:
            self.__dict[prev_elem] = (
                self.__dict[prev_elem][0],
                self.__dict[prev_elem][1],
                next_elem,
            )
        else:
            self._logger.debug("key=`%s` is first in list", key)
            self.__first_elem = next_elem
        if next_elem:
            self.__dict[next_elem] = (
                self.__dict[next_elem][0],
                prev_elem,
                self.__dict[next_elem][2],
            )
        else:
            self._logger.debug("key=`%s` is last in list", key)
            self.__last_elem = prev_elem

        del self.__dict[key]

    def __getitem__(self, key: str) -> Any:
        if key not in self.__dict:
            self._logger.warning("key = `%s` not in a cache", key)
            return None

        value = self.__dict[key][0]
        self.__update_dict(key)

        self._logger.info("key = `%s` has value = `%s`", key, value)
        return value

    def __setitem__(self, key: str, value: str) -> None:
        if not self.__dict.keys():
            self._logger.info("key = %s, value = %s set as the first", key, value)
            self.__dict[key] = (value, "", "")
            self.__first_elem = key
            self.__last_elem = key
        else:
            if key in self.__dict:
                self._logger.info("key=`%s` is exist, start set new value", key)
                self.__remove_from_dict(key)
                self._logger.warning("for key=`%s` set new val=`%s`", key, value)
            else:
                self._logger.info("key=`%s` not exist, set value %s", key, value)

            self.__dict[self.__last_elem] = (
                self.__dict[self.__last_elem][0],
                self.__dict[self.__last_elem][1],
                key,
            )

            self.__dict[key] = (value, self.__last_elem, "")
            self.__last_elem = key
            if self.__limit < len(self.__dict.keys()):
                self._logger.warning(
                    "limit=`%s` reached, key=`%s` deleted after set new key",
                    self.__limit,
                    self.__first_elem,
                )
                self.__remove_from_dict(self.__first_elem)

    @staticmethod
    def _create_logger(stdout_flag: bool, filter_flag: bool):

        logger = logging.getLogger("cache_loger")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        stream_formatter = logging.Formatter(
            "|STREAM|\t%(asctime)s\t%(levelname)s\t%(message)s"
        )

        file_formatter = logging.Formatter(
            datefmt="%Y-%m-%d %H:%M:%S",
            fmt="|FILE|\t[%(asctime)s]\t[%(levelname)s]\t[%(name)s]:\t%(message)s",
        )

        file_handler = logging.FileHandler("cache_log.log", mode="w")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)

        if stdout_flag:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(stream_formatter)

            if filter_flag:
                stream_handler.addFilter(CacheFilter())

            logger.addHandler(stream_handler)

        if filter_flag:
            file_handler.addFilter(CacheFilter())

        logger.addHandler(file_handler)

        return logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LRUCache with logging")

    parser.add_argument(
        "-f",
        "--filter",
        help="enable filter of log message",
        nargs="?",
        const=True,
        default=False,
    )
    parser.add_argument(
        "-s",
        "--stdout",
        help="add logging to stdout",
        nargs="?",
        const=True,
        default=False,
    )

    args = vars(parser.parse_args())

    cache = LRUCache(
        limit=3, enable_stdout=args["stdout"], enable_filter=args["filter"]
    )

    cache["k1"] = "val1"
    cache["k2"] = "val2"
    cache["k3"] = "val3"
    cache["k3"] = "new_val3"
    cache["k4"] = "val4"
    value1 = cache["k1"]
    value2 = cache["k2"]
