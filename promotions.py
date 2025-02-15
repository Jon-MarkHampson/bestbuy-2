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
        if not (0 <= discount_percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")
        super().__init__(name)
        self.discount_percentage = discount_percentage

    def apply_promotion(self, product, quantity) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1 to apply promotion.")
        return (product.price * quantity) * ((100 - self.discount_percentage) / 100)


class SecondItemHalfPrice(Promotion):
    """Applies a half-price discount on the second item."""

    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1 to apply promotion.")

        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2

        total_price = (full_price_items * product.price) + (half_price_items * (product.price / 2))
        # Ensure price is never negative
        return max(total_price, 0)


class BuyTwoGetOneFree(Promotion):
    """Applies a 'buy 2, get 1 free' promotion."""

    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1 to apply promotion.")

        payable_items = (quantity // 3) * 2 + (quantity % 3)
        total_price = payable_items * product.price
        # Ensure price is never negative
        return max(total_price, 0)
