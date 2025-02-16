import products
import store
import promotions
from text_colour_helper import txt_clr


def start(product_list):
    """
    Initializes and returns a Store instance with the given product list.
    """
    return store.Store(product_list)


def show_user_menu():
    """
    Returns the menu as a string for display to the user.
    """
    return f"""\n
---------- {txt_clr.LW}Store Menu{txt_clr.RESET} -----------
_________________________________

1. List all products in store
2. Show total amount in store
3. Make an order
4. {txt_clr.LR}Quit{txt_clr.RESET}
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


def get_all_products_in_store(store_obj, exclude_shipping=False):
    """
    Returns a list all active products in the store. Optionally excludes shipping.
    """
    products_in_store = store_obj.get_all_products()
    if exclude_shipping:
        products_in_store = [p for p in products_in_store if not isinstance(p, products.Shipping)]
    return products_in_store


def print_all_products_in_store(products_in_store):
    """
    Prints all active products in the store. Optionally excludes shipping.
    """
    if not products_in_store:
        print("No active products in store.")
    else:
        for idx, product in enumerate(products_in_store, start=1):
            print(f"{idx}. {product}")


def display_all_products_in_store(store_obj, exclude_shipping=False):
    """
    Lists all active products in the store and prints them out to the console.
    """
    products_in_store = get_all_products_in_store(store_obj, exclude_shipping)
    print(f"\n-------------{txt_clr.LW} All Products in Store{txt_clr.RESET} -------------")
    print("_________________________________________________\n")
    print_all_products_in_store(products_in_store)
    print("_________________________________________________")


def show_total_amount_in_store(store_obj):
    """
    Prints out the total sum of quantities of all products in the store.
    """
    total_quantity = store_obj.get_total_quantity()
    print("___________________________________________")
    print(f"\n{txt_clr.LW}Total amount of all products in store: {txt_clr.LB}{total_quantity}{txt_clr.RESET}")
    print("___________________________________________")


def show_shopping_cart(shopping_list):
    """
    Prints out the current contents of the shopping cart.
    """
    print(f"\n-------------{txt_clr.LW} All Items in Shopping Cart{txt_clr.RESET} -------------")
    print("_________________________________________________\n")
    if not shopping_list:
        print(f"{txt_clr.LR}\tNo items in shopping cart.{txt_clr.RESET}")
    else:
        for idx, product in enumerate(shopping_list, start=1):
            print(f"{idx}. {product}")
    print("_________________________________________________")


def make_an_order(store_obj):
    """
    Prompts the user to make an order, allowing them to add multiple items before completing the purchase.
    """
    order_incomplete = True
    shopping_list = []
    shipping_added = False  # Track whether shipping has been added

    while order_incomplete:

        invalid_order_quantity = True

        while invalid_order_quantity:
            # Exclude shipping from the list if it's already in the shopping cart
            products_in_store = get_all_products_in_store(store_obj, exclude_shipping=shipping_added)
            complete_order_choice = len(products_in_store) + 1
            show_shopping_cart_choice = len(products_in_store) + 2
            exit_ordering_choice = len(products_in_store) + 3

            print(f"\n--------------------- {txt_clr.LW}Make an Order{txt_clr.RESET} -------------------")
            print("_______________________________________________________\n")
            print_all_products_in_store(products_in_store)
            print(f"{complete_order_choice}. {txt_clr.LB}Complete Current Order{txt_clr.RESET}")
            print(f"{show_shopping_cart_choice}. {txt_clr.LC}Show Shopping Cart Contents{txt_clr.RESET}")
            print(f"{exit_ordering_choice}. {txt_clr.LR}Exit Ordering Process{txt_clr.RESET}")
            print("_______________________________________________________")

            # Get valid product selection
            choice = get_valid_int_input("\nEnter product number: ", 1, len(products_in_store) + 3)

            if choice == exit_ordering_choice:
                return None
            elif choice == show_shopping_cart_choice:
                show_shopping_cart(shopping_list)
                continue
            elif choice == complete_order_choice:
                break

            chosen_product = products_in_store[choice - 1]

            # If user selects shipping, add it with quantity 1 and prevent re-selection
            if isinstance(chosen_product, products.Shipping):
                if not shipping_added:  # Ensure shipping is not added twice
                    shopping_list.append((chosen_product, 1))
                    print(f"{txt_clr.LY}Shipping added to shopping cart.{txt_clr.RESET}")
                    shipping_added = True  # Prevent shipping from appearing again
                continue  # Skip asking for quantity

            # For all other products, get valid quantity
            chosen_product_stock_quantity = chosen_product.quantity
            order_quantity = get_valid_int_input(f"Enter quantity for {chosen_product.name}: ", 1)

            if isinstance(chosen_product, products.NonStockedProduct):
                invalid_order_quantity = False
            else:
                if order_quantity <= chosen_product_stock_quantity:
                    invalid_order_quantity = False
                else:
                    print(
                        f"Insufficient stock for an order of {txt_clr.LR}{order_quantity}{txt_clr.RESET}, "
                        f"only {txt_clr.LB}{chosen_product_stock_quantity}{txt_clr.RESET} available."
                    )

        shopping_list.append((chosen_product, order_quantity))
        print(f"{chosen_product.name} (quantity {txt_clr.LB}{order_quantity}{txt_clr.RESET}) added to shopping cart.")

        # Ask if user wants to add more items
        more_items = input("Do you want to add another item? (yes/no): ").strip().lower()
        if more_items not in {"y", "yes", "yeah", "yep", "yup"}:
            break

    # Check if shipping is needed
    shopping_list = check_and_offer_shipping(shopping_list, shipping_added)

    # Attempt the purchase
    try:
        total_price = store_obj.order(shopping_list)
        print(f"Order successful! Total cost: ${txt_clr.LG}{total_price:.2f}{txt_clr.RESET}")
    except Exception as e:
        print(f"Order failed: {str(e)}")



def check_and_offer_shipping(shopping_list, shipping_added):
    """
    Checks if shipping is needed and offers it to the user.
    - Only offers shipping if there are physical products (`Product` but not `NonStockedProduct`).
    - Does not offer shipping if it's already in the order.
    """
    has_physical_products = any(
        isinstance(item[0], products.Product) and not isinstance(item[0], products.NonStockedProduct)
        for item in shopping_list
    )

    # Ensure shipping isn't added twice
    if has_physical_products and not shipping_added:
        need_shipping = input("Do you need shipping? (yes/no): ").strip().lower()
        if need_shipping in {"y", "yes"}:
            shipping_option = products.Shipping("Standard Shipping", price=10)
            shopping_list.append((shipping_option, 1))
            print(f"{txt_clr.LY}Shipping added to shopping cart.{txt_clr.RESET}")

    return shopping_list


def main():
    # Setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.Product("Sony WH-1000XM5", price=350, quantity=300),
        products.Product("iPad Pro", price=1200, quantity=150),
        products.Product("Dell XPS 13", price=1400, quantity=200),
        products.NonStockedProduct("Windows License", price=125),
        products.NonStockedProduct("Adobe Photoshop Subscription", price=20),
        products.LimitedProduct("Extended Warranty", price=100, quantity=500, purchase_limit=1),
        products.LimitedProduct("Gift Wrapping", price=5, quantity=1000, purchase_limit=1),
        products.Shipping("Standard Shipping", price=10)
    ]

    # Create promotion catalog
    second_half_price = promotions.SecondItemHalfPrice("Second Half Price!")
    third_one_free = promotions.BuyTwoGetOneFree("Third One Free!")
    thirty_percent = promotions.PercentageDiscount("30% off!", discount_percentage=30)

    # Add promotions to products
    product_list[0].promotion = second_half_price
    product_list[1].promotion = third_one_free
    product_list[2].promotion = thirty_percent
    product_list[3].promotion = thirty_percent
    product_list[4].promotion = third_one_free

    best_buy = start(product_list)

    # Dispatcher mapping each menu choice to a function
    dispatcher = {
        "1": lambda: display_all_products_in_store(best_buy),
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
