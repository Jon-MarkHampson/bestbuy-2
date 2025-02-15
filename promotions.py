from abc import ABC, abstractmethod


class Promotion(ABC):
    """Abstract base class for promotions."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass


class PercentageDiscount(Promotion):
    """Applies a percentage discount to a product."""

    def __init__(self, name: str, discount_percentage: float):
        super().__init__(name)
        self.discount_percentage = discount_percentage

    def apply_promotion(self, product, quantity) -> float:
        return (product.price * quantity) * ((100 - self.discount_percentage) / 100)


class SecondItemHalfPrice(Promotion):
    """Applies a half-price discount on the second item."""

    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return (full_price_items * product.price) + (half_price_items * (product.price / 2))


class BuyTwoGetOneFree(Promotion):
    """Applies a 'buy 2, get 1 free' promotion."""

    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        payable_items = (quantity // 3) * 2 + (quantity % 3)
        return payable_items * product.price
