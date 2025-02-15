class Store:
    """This Store class manages all product instances and provides functionality for inventory management."""

    def __init__(self, products_list: list):
        """Initializes the store with a list of products."""
        self._products_list = products_list

    @property
    def products_list(self):
        """Returns the list of products in the store."""
        return self._products_list

    def add_product(self, product):
        """Adds a new product to the store."""
        if product not in self._products_list:
            self._products_list.append(product)

    def remove_product(self, product):
        """Removes a product from the store if it exists."""
        if product in self._products_list:
            self._products_list.remove(product)

    def get_total_quantity(self) -> int:
        """Gets the total quantity of all products in the store (sum of all product quantities)."""
        return sum(product.quantity for product in self._products_list)

    def get_all_products(self) -> list:
        """Returns a list of all active products in the store.
        A product is considered active if product.active == True.
        """
        return [product for product in self._products_list if product.active]

    def order(self, shopping_list: list) -> float:
        """Processes the purchase of multiple products."""
        total_price = 0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price

    def __contains__(self, product):
        """Allows checking if a product exists in the store using the 'in' operator."""
        return product in self._products_list

    def __str__(self):
        """Returns a formatted string of all products in the store."""
        return "\n".join(str(product) for product in self._products_list)

    def __repr__(self):
        """Returns a debug-friendly representation of the store."""
        return f"Store({self._products_list})"

    def __add__(self, other):
        """Combines two stores into a new store containing all products from both."""
        if not isinstance(other, Store):
            return NotImplemented
        return Store(self._products_list + other._products_list)
