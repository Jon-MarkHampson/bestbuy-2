import store
from promotions import Promotion
from text_colour_helper import txt_clr


class Product:
    """Represents a product with a name, price, quantity, and active status."""

    def __init__(self, name: str, price: float, quantity: int, promotion: Promotion = None):
        """Initializes the Product instance with name, price, quantity, and an optional promotion."""
        if not name:
            raise ValueError("The name cannot be empty.")
        if price is None or price < 0:
            raise ValueError("The price must be a non-negative value.")
        if quantity is None or quantity < 0:
            raise ValueError("The quantity must be a non-negative value.")

        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = True
        self._promotion = promotion

    @property
    def name(self):
        """Returns the name of the product."""
        return self._name

    @property
    def quantity(self):
        """Returns the current quantity of the product."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """Sets the product's quantity and deactivates it if the quantity reaches 0."""
        if value < 0:
            raise ValueError("The quantity must be non-negative.")
        self._quantity = value
        self._active = value > 0

    @property
    def promotion(self):
        """Returns the promotion applied to the product."""
        return self._promotion

    @promotion.setter
    def promotion(self, promotion: Promotion):
        """Sets the promotion for the product."""
        self._promotion = promotion

    @property
    def price(self):
        """Returns the price of the product."""
        return self._price

    @price.setter
    def price(self, value):
        """Sets the price of the product and ensures it is not negative."""
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def active(self) -> bool:
        """Returns whether the product is active."""
        return self._active

    def activate(self):
        """Activates the product."""
        self._active = True

    def deactivate(self):
        """Deactivates the product."""
        self._active = False

    def __str__(self) -> str:
        """Returns a formatted string representation of the product."""
        promotion_info = f" | Promotion: {txt_clr.LR}{self.promotion.name}{txt_clr.RESET}" if self.promotion else ""
        return f"Product: {txt_clr.LY}{self._name}{txt_clr.RESET} | Price: ${txt_clr.LG}{self._price:.2f}{txt_clr.RESET} | Quantity: {txt_clr.LB}{self._quantity}{txt_clr.RESET} | Active: {txt_clr.LM}{self._active}{txt_clr.RESET}{promotion_info}"

    def __repr__(self) -> str:
        """Returns a string representation useful for debugging."""
        return self.__str__()

    def __gt__(self, other):
        """Compares products based on price."""
        if not isinstance(other, Product):
            return NotImplemented
        return self._price > other._price

    def __lt__(self, other):
        """Compares products based on price."""
        if not isinstance(other, Product):
            return NotImplemented
        return self._price < other._price

    def buy(self, quantity: int) -> float:
        """Buys a given quantity of the product and returns the total price.
        Ensures valid stock availability before purchase."""
        if not self._active:
            raise Exception("Cannot buy this product because it is inactive.")
        if quantity <= 0:
            raise ValueError("The quantity to buy must be greater than 0.")
        if quantity > self._quantity:
            raise ValueError(f"Insufficient stock to complete the purchase. Available: {self._quantity}")

        total_price = self._promotion.apply_promotion(self, quantity) if self._promotion else self._price * quantity
        self.quantity -= quantity
        return total_price


class NonStockedProduct(Product):
    """Represents a product that has no stock tracking (e.g., digital products)."""

    def __init__(self, name: str, price: float):
        """Initializes a non-stocked product with a fixed quantity of 0."""
        super().__init__(name, price, quantity=0)

    @property
    def quantity(self):
        """Returns 0 as non-stocked products do not have a quantity."""
        return 0

    @quantity.setter
    def quantity(self, value):
        """Prevents modification of quantity for non-stocked products."""
        raise ValueError("Non-stocked products cannot have a quantity.")

    def __str__(self) -> str:
        """Returns a formatted string representation of the non-stocked product."""
        promotion_info = f" | Promotion: {txt_clr.LR}{self.promotion.name}{txt_clr.RESET}" if self.promotion else ""
        return f"Non Stocked Product: {txt_clr.LY}{self._name}{txt_clr.RESET} | Price: ${txt_clr.LG}{self._price:.2f}{txt_clr.RESET} | Active: {txt_clr.LM}{self._active}{txt_clr.RESET}{promotion_info}"

    def buy(self, quantity: int) -> float:
        """Ensures that the purchasing does not reduce non-stocked quantity of zero."""
        return self.price * quantity


class LimitedProduct(Product):
    """Represents a product with a purchase limit per order."""

    def __init__(self, name: str, price: float, quantity: int, purchase_limit: int):
        """Initializes a limited product with a maximum purchase limit per order."""
        super().__init__(name, price, quantity)
        if purchase_limit < 1:
            raise ValueError("Purchase limit must be at least 1.")
        self.purchase_limit = purchase_limit

    def buy(self, quantity: int) -> float:
        """Ensures that the purchase quantity does not exceed the limit."""
        if quantity > self.purchase_limit:
            raise ValueError(f"Cannot purchase more than {self.purchase_limit} of this product per order.")
        return super().buy(quantity)

    def __str__(self) -> str:
        """Returns a formatted string representation of the limited product."""
        promotion_info = f" | Promotion: {txt_clr.LR}{self.promotion.name}{txt_clr.RESET}" if self.promotion else ""
        return f"Limited Product: {txt_clr.LY}{self._name}{txt_clr.RESET} | Price: ${txt_clr.LG}{self._price:.2f}{txt_clr.RESET} | Active: {txt_clr.LM}{self._active}{txt_clr.RESET}{promotion_info} | Purchase Limit: {txt_clr.LC}{self.purchase_limit}{txt_clr.RESET}"


class AddOns(LimitedProduct):
    """Represents a shipping product with a one-time purchase limit per order."""

    def __init__(self, name: str, price: float):
        """Initializes a shipping item with a purchase limit of 1."""
        super().__init__(name, price, quantity=1, purchase_limit=1)

    @property
    def quantity(self):
        """Returns a fixed quantity of 1 for shipping since it is always available."""
        return 1

    @quantity.setter
    def quantity(self, value):
        """Prevents modifying the shipping quantity."""
        raise ValueError("Quantity cannot be modified.")

    def __str__(self) -> str:
        """Returns a formatted string representation of the shipping."""
        return f"Add On: {txt_clr.LY}{self.name}{txt_clr.RESET} | Price: ${txt_clr.LB}{self.price:.2f}{txt_clr.RESET} | {txt_clr.LC}One-time purchase per order{txt_clr.RESET}"

    def buy(self, quantity: int) -> float:
        """Ensures that the purchase quantity does not exceed the limit."""
        if quantity > self.purchase_limit:
            raise ValueError(f"Cannot purchase more than {self.purchase_limit} of this product per order.")
        return self._price


if __name__ == "__main__":
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = Product("Google Pixel 7", price=500, quantity=250)

    best_buy = store.Store([mac, bose])
    try:
        mac.price = -100  # Should raise ValueError
    except ValueError as e:
        print(e)
    print(mac)  # Should print `MacBook Air M2, Price: $1450 Quantity:100`
    print(mac > bose)  # Should print True
    print(mac in best_buy)  # Should print True
    print(pixel in best_buy)  # Should print False

    for product in best_buy.products_list:
        print(product)
