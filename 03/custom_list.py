class CustomList(list):
    def __add__(self, list2):
        res = []
        list_left = self.copy()
        list_right = list2.copy()

        if len(list2) < len(self):
            list_right += [0] * (len(self) - len(list2))
        else:
            list_left += [0] * (-len(self) + len(list2))

        for i, elem_left in enumerate(list_left):
            res += [elem_left + list_right[i]]

        return CustomList(res)

    def __radd__(self, list2):
        res = []
        list_left = self.copy()
        list_right = list2.copy()

        if len(list2) < len(self):
            list_right += [0] * (len(self) - len(list2))
        else:
            list_left += [0] * (-len(self) + len(list2))

        for i, elem_left in enumerate(list_left):
            res += [elem_left + list_right[i]]

        return CustomList(res)

    def __sub__(self, list2):
        res = []
        list_left = self.copy()
        list_right = list2.copy()

        if len(list2) < len(self):
            list_right += [0] * (len(self) - len(list2))
        else:
            list_left += [0] * (-len(self) + len(list2))

        for i, elem_left in enumerate(list_left):
            res += [elem_left - list_right[i]]

        return CustomList(res)

    def __rsub__(self, list2):
        res = []
        list_left = self.copy()
        list_right = list2.copy()

        if len(list2) < len(self):
            list_right += [0] * (len(self) - len(list2))
        else:
            list_left += [0] * (-len(self) + len(list2))

        for i, elem_left in enumerate(list_left):
            res += [list_right[i] - elem_left]

        return CustomList(res)

    def __eq__(self, list2):
        return sum(self) == sum(list2)

    def __ne__(self, list2):
        return sum(self) != sum(list2)

    def __lt__(self, list2):
        return sum(self) < sum(list2)

    def __le__(self, list2):
        return sum(self) <= sum(list2)

    def __gt__(self, list2):
        return sum(self) > sum(list2)

    def __ge__(self, list2):
        return sum(self) >= sum(list2)

    def __str__(self):
        return f"|{self[:]}, sum = {sum(self)}|"
