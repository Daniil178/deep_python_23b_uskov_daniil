from io import StringIO, TextIOBase
import re


class FilterFile:
    def __init__(
            self,
            filename: str = "",
            file_object: TextIOBase = StringIO('')
    ):
        if not isinstance(filename, str):
            raise TypeError("filename is not string")

        if (filename == "") and not isinstance(file_object, TextIOBase):
            raise TypeError("file object is not TextIO")

        self.filename = filename

        if filename:
            self.file = open(filename, "r", encoding="utf-8")
        else:
            self.file = file_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.filename:
            self.file.close()

    def filter_text(self, key_words: list[str]) -> str:
        for line in self.file:
            line_low = line.lower()
            for key_word in key_words:
                if re.search(
                        ('\\b' + key_word.lower() + '\\b'),
                        line_low):
                    yield line
                    break
