from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.protected_name = f"_{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.protected_name, None)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be less than {self.min_value} and greater than {self.max_value}")

    pass


class OneOf(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {tuple(self.options)}.")

    pass


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)

    sauce = OneOf(["ketchup", "mayo", "burger"])

    def __init__(self, buns, cheese, tomatoes, cutlets, eggs, sauce):
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce

    print("Burger will be created")
