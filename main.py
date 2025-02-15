import products
import store


def start(product_list):
    """
    Initializes and returns a Store instance with the given product list.
    """
    return store.Store(product_list)


def show_user_menu():
    """
    Returns the menu as a string for display to the user.
    """
    return """\n
-----------Store Menu------------
_________________________________

1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit
_________________________________

Please choose a number: """


def get_valid_int_input(prompt, min_val=None, max_val=None):
    """
    Reusable function to get valid integer input within an optional range.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            value = int(user_input)
            if (min_val is None or value >= min_val) and (max_val is None or value <= max_val):
                return value
            print(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_user_input():
    """
    Prompts the user to select a menu option (1-4) and returns the valid choice as a string.
    """
    return str(get_valid_int_input(show_user_menu(), 1, 4))


def list_all_products_in_store(store_obj):
    """
    Lists all active products in the store and prints them out to the console.
    """
    products_in_store = store_obj.get_all_products()
    print("\n------------- All Products in Store -------------")
    print("_________________________________________________\n")

    if not products_in_store:
        print("No active products in store.")
    else:
        for idx, product in enumerate(products_in_store, start=1):
            print(f"{idx}. {product}")

    print("_________________________________________________\n")


def show_total_amount_in_store(store_obj):
    """
    Prints out the total sum of quantities of all products in the store.
    """
    total_quantity = store_obj.get_total_quantity()
    print("___________________________________________")
    print(f"\nTotal amount of all products in store: {total_quantity}")
    print("___________________________________________")


def make_an_order(store_obj):
    """
    Prompts the user to make an order:
      1) Shows all products.
      2) Asks the user to select one product (by number).
      3) Asks the user for the quantity to buy.
      4) Attempts to order; prints success or error message.
    """
    products_in_store = store_obj.get_all_products()
    if not products_in_store:
        print("No active products to order.")
        return

    print("\n--------------------- Make an Order -------------------")
    print("_______________________________________________________\n")
    for index, product in enumerate(products_in_store, start=1):
        print(f"{index}. {product.name} (Price: ${product.price}, Stock: {product.quantity})")
    print("_______________________________________________________")

    # Get valid product selection
    choice = get_valid_int_input("\nEnter product number: ", 1, len(products_in_store))
    chosen_product = products_in_store[choice - 1]

    # Get valid quantity
    quantity = get_valid_int_input(f"Enter quantity for {chosen_product.name}: ", 1)

    # Attempt the purchase
    try:
        total_price = store_obj.order([(chosen_product, quantity)])
        print(f"Order successful! {quantity} of {chosen_product.name} - Total cost: ${total_price:.2f}")
    except Exception as e:
        print(f"Order failed: {str(e)}")


def main():
    # Setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250)
    ]

    best_buy = start(product_list)

    # Dispatcher mapping each menu choice to a function
    dispatcher = {
        "1": lambda: list_all_products_in_store(best_buy),
        "2": lambda: show_total_amount_in_store(best_buy),
        "3": lambda: make_an_order(best_buy)
    }

    print("Welcome to the Best Buy Store!")

    while True:
        user_menu_choice = get_user_input()

        if user_menu_choice == "4":
            print("\n________________________________")
            print("\nThank you for visiting! Goodbye.")
            print("________________________________\n")
            break

        action_function = dispatcher.get(user_menu_choice)
        if action_function:
            action_function()


if __name__ == "__main__":
    main()
