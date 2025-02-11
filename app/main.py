from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: any, name: any) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: any, owner: any) -> None:
        return getattr(instance, self.protected_name, None)

    def __set__(self, instance: any, value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}"
            )

    pass


class OneOf(Validator):
    def __init__(self, options: any) -> None:
        self.options = options

    def validate(self, value: int) -> None:
        if value not in self.options:
            raise (ValueError
                  (f"Expected {value} to be one of {tuple(self.options)}."))

    pass


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)

    sauce = OneOf(["ketchup", "mayo", "burger"])

    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 sauce: list) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
