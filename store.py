class Store:
    """This Store class will contain all the instances of the Product class."""

    def __init__(self, products_list):
        """
        Initialize the store with a list of products.
        :param products_list: list of Product instances
        """
        self.products_list = products_list

    def add_product(self, product):
        """Adds a new product to the store."""
        self.products_list.append(product)

    def remove_product(self, product):
        """Removes a product from the store."""
        self.products_list.remove(product)

    def get_total_quantity(self) -> int:
        """
        Gets the total quantity of all products in the store (sum of all product quantities).
        """
        return sum(product.quantity for product in self.products_list)

    def get_all_products(self) -> list:
        """
        Returns a list of all active products in the store.
        A product is considered active if product.active == True.
        """
        return [product for product in self.products_list if product.is_active()]

    def order(self, shopping_list) -> float:
        """
        Takes a list of (Product, quantity) tuples and processes the purchase,
        returning the total price. Will raise exceptions if insufficient stock
        or the product is inactive.
        """
        total_price = 0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)  # product.buy() updates the product's stock
        return total_price
