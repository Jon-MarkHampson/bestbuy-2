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

    def show(self) -> str:
        """Returns a string representation of the product."""
        return f"Product: {self.name}, Price: ${self.price:.2f}, Quantity: {self.quantity}, Active: {self.active}"

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
            raise Exception(f"Insufficient stock to complete the purchase. Available: {self.quantity}")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)  # Updates quantity & deactivates if it hits 0
        return total_price
