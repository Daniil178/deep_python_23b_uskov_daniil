def custom_setattr(self, name, val):
    if name.find("__") != -1:
        ind = name.index("__")
        self.__dict__[f"{name[:ind + 2]}custom_{name[ind + 2:]}"] = val
    elif name[0] == "_":
        self.__dict__["_custom" + name] = val
    else:
        self.__dict__["custom_" + name] = val


class CustomMeta(type):
    def __new__(mcs, name, bases, classdict, **kwargs):
        new_dict = {}

        for method in classdict:
            if (method[0:2] + method[-1:-3:-1]) != "____":
                if method.find("__") != -1:
                    new_dict[f"_{name}__custom_" + method[len(name) + 3:]] \
                        = classdict[method]
                elif method[0] == "_":
                    new_dict["_custom" + method] = classdict[method]
                else:
                    new_dict["custom_" + method] = classdict[method]
            else:
                new_dict[method] = classdict[method]

        new_dict["__setattr__"] = custom_setattr
        cls = super().__new__(mcs, name, bases, new_dict)

        return cls

    def __init__(cls, name, bases, classdict, **kwargs):
        super().__init__(name, bases, classdict, **kwargs)
