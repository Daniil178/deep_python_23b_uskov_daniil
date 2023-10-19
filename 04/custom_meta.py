def custom_setattr(self, name, val):
    name_attr = ""
    if name.find("custom") == -1:
        if name[0:2] + name[-1:-3:-1] != "____":
            if name.find("__") != -1:
                ind = name.index("__")
                name_attr = f"{name[:ind + 2]}custom_{name[ind + 2:]}"
            elif name[0] == "_":
                name_attr = "_custom" + name
            else:
                name_attr = "custom_" + name
        else:
            name_attr = name
    else:
        self.__dict__[name] = val

    if not (
        (name_attr in self.__class__.__dict__.keys()) or
        (name_attr in self.__dict__.keys())
    ):
        self.__dict__[name_attr] = val


class CustomMeta(type):
    def __new__(mcs, name, bases, classdict, **kwargs):
        new_dict = {}

        for method in classdict:
            if (method[0:2] + method[-1:-3:-1]) != "____":
                if method.find("__") != -1:
                    new_dict[f"_{name}__custom_" + method[len(name) + 3 :]] = classdict[
                        method
                    ]
                elif method[0] == "_":
                    new_dict["_custom" + method] = classdict[method]
                else:
                    new_dict["custom_" + method] = classdict[method]
            else:
                new_dict[method] = classdict[method]

        new_dict["__setattr__"] = custom_setattr
        cls = super().__new__(mcs, name, bases, new_dict)

        return cls

    def __setattr__(self, name, val):
        name_attr = ""
   
        if name.find("custom") == -1:
            if name[0:2] + name[-1:-3:-1] != "____":
                if name.find("__") != -1:
                    ind = name.index("__")
                    name_attr = f"{name[:ind + 2]}custom_{name[ind + 2:]}"
                elif name[0] == "_":
                    name_attr = "_custom" + name
                else:
                    name_attr = "custom_" + name
            else:
                name_attr = name
        else:
            super().__setattr__(name, val)

        if not (
                (name_attr in self.__class__.__dict__.keys()) or
                (name_attr in self.__dict__.keys())
        ):
            super().__setattr__(name_attr, val)
