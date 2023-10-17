import re


class StrTemplate:
    def __init__(self, template: str):
        if not isinstance(template, str):
            raise TypeError("str required for template")

        self.template = template

    def __set_name__(self, owner, name):
        self.name = f"str_template_descr_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, str):
            raise TypeError("str required")

        if not re.fullmatch(self.template, val):
            raise ValueError("value don't equal of template")

        return setattr(obj, self.name, val)


class FixNumber:
    def __init__(self, low_border, high_border):
        if not (isinstance(low_border, (int, float))
                and isinstance(high_border, (int, float))):
            raise TypeError("borders is float or int number")

        self.low_border = low_border
        self.high_border = high_border

    def __set_name__(self, owner, name):
        self.name = f"number_template_descr_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, (int, float)):
            raise TypeError("float or int required")

        if self.low_border > val or val > self.high_border:
            raise ValueError("value don't equal of template")

        return setattr(obj, self.name, val)


class ChoiceList:
    def __init__(self, choice_list: list):
        if not isinstance(choice_list, list):
            raise TypeError("choice list is list")

        if choice_list is None:
            choice_list = []

        self.choice_list = choice_list

    def __set_name__(self, owner, name):
        self.name = f"choice_template_descr_{name}"

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        if not isinstance(val, str):
            raise TypeError("str required")

        if val not in self.choice_list:
            raise ValueError("value should in choice list")

        return setattr(obj, self.name, val)
