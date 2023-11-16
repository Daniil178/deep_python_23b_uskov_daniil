import time
import weakref
import cProfile
from memory_profiler import profile


class Passport:
    def __init__(self, series: str = "1234", number: str = "123456"):
        self.series = series
        self.number = number


class ClassWithAttrs:
    def __init__(self, some_set: set, passport: Passport):
        self.some_set = some_set
        self.passport = passport


class ClassWithSlots:
    __slots__ = ("some_set", "passport")

    def __init__(self, some_set: set, passport: Passport):
        self.some_set = some_set
        self.passport = passport


class ClassWithWeakRef:
    def __init__(self, some_set: set, passport: Passport):
        self.some_set = weakref.ref(some_set)
        self.passport = weakref.ref(passport)


@profile
def measure_instance_creation(class_type, num: int = 10**6, count: int = 10) -> float:
    times = []
    for _ in range(count):

        start_time = time.time()
        instances = [class_type(set(), Passport("123", "456")) for __ in range(num)]
        end_time = time.time()

        times += [end_time - start_time]
    return sum(times) / count


def measure_attribute_access(class_type, num: int = 10**6, count: int = 10) -> float:
    instance = class_type(set(), Passport("123", "456"))
    times = []
    for _ in range(count):

        start_time = time.time()
        for i in range(num):
            instance.some_set = {i}
            instance.passport = Passport()
        end_time = time.time()

        times += [end_time - start_time]
    return sum(times) / count


def measure_attribute_read(class_type, num: int = 10**6, count: int = 10) -> float:
    instance = class_type(set(), Passport("123", "456"))
    times = []
    for _ in range(count):

        start_time = time.time()
        for __ in range(num):
            some_set = instance.some_set
            passport = instance.passport

        end_time = time.time()

        times += [end_time - start_time]
    return sum(times) / count


def compare_time() -> None:
    creation_time_attrs = measure_instance_creation(ClassWithAttrs)
    creation_time_slots = measure_instance_creation(ClassWithSlots)
    creation_time_weakref = measure_instance_creation(ClassWithWeakRef)

    print("Время создания экземпляров:")
    print(f"ClassWithAttrs: {creation_time_attrs} seconds")
    print(f"ClassWithSlots: {creation_time_slots} seconds")
    print(f"ClassWithWeakRef: {creation_time_weakref} seconds")

    access_time_attrs = measure_attribute_access(ClassWithAttrs)
    access_time_slots = measure_attribute_access(ClassWithSlots)
    access_time_weakref = measure_attribute_access(ClassWithWeakRef)

    print("\nВремя изменения атрибутов:")
    print(f"ClassWithAttrs: {access_time_attrs} seconds")
    print(f"ClassWithSlots: {access_time_slots} seconds")
    print(f"ClassWithWeakRef: {access_time_weakref} seconds")

    read_time_attrs = measure_attribute_read(ClassWithAttrs)
    read_time_slots = measure_attribute_read(ClassWithSlots)
    read_time_weakref = measure_attribute_read(ClassWithWeakRef)

    print("\nВремя чтения атрибутов:")
    print(f"ClassWithAttrs: {read_time_attrs} seconds")
    print(f"ClassWithSlots: {read_time_slots} seconds")
    print(f"ClassWithWeakRef: {read_time_weakref} seconds")


def compare_memory_calls() -> None:

    cProfile.run("measure_instance_creation(ClassWithAttrs)")
    cProfile.run("measure_instance_creation(ClassWithSlots)")
    cProfile.run("measure_instance_creation(ClassWithWeakRef)")

    measure_instance_creation(ClassWithAttrs)
    measure_instance_creation(ClassWithSlots)
    measure_instance_creation(ClassWithWeakRef)


if __name__ == "__main__":
    # compare_time()
    compare_memory_calls()
