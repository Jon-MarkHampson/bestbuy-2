import store


class Product:
    """Represents a product with a name, price, quantity, and active status."""

    def __init__(self, name: str, price: float, quantity: int):
        """Initializes the Product instance with name, price, and quantity."""
        if not name:
            raise ValueError("The name cannot be empty.")
        if price is None or price < 0:
            raise ValueError("The price must be a non-negative value.")
        if quantity is None or quantity < 0:
            raise ValueError("The quantity must be a non-negative value.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> float:
        """Returns the current quantity of the product."""
        return float(self.quantity)

    def set_quantity(self, quantity: int):
        """
        Sets the product's quantity.
        Deactivates the product if quantity reaches 0.
        """
        if quantity < 0:
            raise ValueError("The quantity must be non-negative.")

        self.quantity = quantity

        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Returns whether the product is active."""
        return self.active

    def activate(self):
        """Activates the product."""
        self.active = True

    def deactivate(self):
        """Deactivates the product."""
        self.active = False

    def show(self):
        """Returns a user-friendly string representation of the product."""
        return str(self)

    def __str__(self) -> str:
        """Returns a formatted string representation of the product."""
        return f"Product: {self.name} | Price: ${self.price:.2f} | Quantity: {self.quantity} | Active: {self.active}"

    def __repr__(self) -> str:
        """Returns a string representation useful for debugging and lists."""
        return f"Product({self.name!r}, Price: ${self.price:.2f}, Quantity: {self.quantity}, Active: {self.active})"

    def buy(self, quantity: int) -> float:
        """
        Buys a given quantity of the product and returns the total price.
        Raises an exception if the product is inactive, the quantity is <= 0,
        or there is insufficient stock.
        """
        if not self.active:
            raise Exception("Cannot buy this product because it is inactive.")
        if quantity <= 0:
            raise ValueError("The quantity to buy must be greater than 0.")
        if quantity > self.quantity:
            raise ValueError(f"Insufficient stock to complete the purchase. Available: {self.quantity}")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)  # Updates quantity & deactivates if it hits 0
        return total_price


class NonStockedProduct(Product):
    """Represents a product that has no stock tracking (e.g., digital products)."""

    def __init__(self, name: str, price: float):
        """Initializes a non-stocked product with a fixed quantity of 0."""
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int):
        """Overrides set_quantity to prevent modification of quantity"""
        raise ValueError("Non-stocked products cannot have a quantity.")

    def __str__(self) -> str:
        """Returns a human-friendly string representation of non-stocked products."""
        return f"Non-Stocked Product: {self.name} | Price: ${self.price:.2f}"

    def __repr__(self) -> str:
        """Returns a string representation useful for debugging non-stocked products."""
        return f"NonStockedProduct({self.name!r}, {self.price})"

    def show(self) -> str:
        """Returns a formatted string representation specific to non-stocked products."""
        return self.__str__()


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
        """Returns a human-friendly string representation of limited products."""
        return f"Limited Product: {self.name} | Price: ${self.price:.2f} | Quantity: {self.quantity} | Limit per order: {self.purchase_limit}"

    def __repr__(self) -> str:
        """Returns a string representation useful for debugging limited products."""
        return f"LimitedProduct({self.name!r}, {self.price}, {self.quantity}, Limit={self.purchase_limit})"

    def show(self) -> str:
        """Returns a formatted string representation specific to limited products."""
        return self.__str__()


def main():
    # setup initial stock of inventory
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    NonStockedProduct("Windows License", price=125),
                    LimitedProduct("Shipping", price=10, quantity=250, purchase_limit=1)
                    ]
    best_buy = store.Store(product_list)
    for product in best_buy.products_list:
        print(product)


if __name__ == "__main__":
    main()
