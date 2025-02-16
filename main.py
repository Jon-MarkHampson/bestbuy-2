import products
import store
import promotions
from bestbuy.products import Product
from text_colour_helper import txt_clr


def start(product_list):
    """Initializes and returns a Store instance with the given product list."""
    return store.Store(product_list)


def show_user_menu():
    """Returns the menu as a string for display to the user."""
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
    """Reusable function to get valid integer input within an optional range."""
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
    """Prompts the user to select a menu option (1-4) and returns the valid choice as a string."""
    return str(get_valid_int_input(show_user_menu(), 1, 4))


def get_all_products_in_store(store_obj, exclude_shipping=False):
    """Returns a list all active products in the store. Optionally excludes shipping."""
    products_in_store = store_obj.get_all_products()
    if exclude_shipping:
        products_in_store = [p for p in products_in_store if not isinstance(p, products.Shipping)]
    return products_in_store


def print_all_products_in_store(products_in_store):
    """Prints all active products in the store."""
    if not products_in_store:
        print("No active products in store.")
    else:
        for idx, product in enumerate(products_in_store, start=1):
            print(f"{idx}. {product}")


def display_all_products_in_store(store_obj, exclude_shipping=False):
    """Lists all active products in the store and prints them out to the console."""
    products_in_store = get_all_products_in_store(store_obj, exclude_shipping)
    print(f"\n-------------{txt_clr.LW} All Products in Store{txt_clr.RESET} -------------")
    print("_________________________________________________\n")
    print_all_products_in_store(products_in_store)
    print("_________________________________________________")


def show_total_amount_in_store(store_obj):
    """Prints out the total sum of quantities of all products in the store."""
    total_quantity = store_obj.get_total_quantity()
    print("___________________________________________")
    print(f"\n{txt_clr.LW}Total amount of all products in store: {txt_clr.LB}{total_quantity}{txt_clr.RESET}")
    print("___________________________________________")


def show_shopping_cart(shopping_list):
    """Prints out the current contents of the shopping cart."""
    print(f"\n-------------{txt_clr.LW} Current Items in Shopping Cart{txt_clr.RESET} -------------")
    print("_________________________________________________\n")
    if not shopping_list:
        print(f"{txt_clr.LR}\t\t\tNo items in shopping cart.{txt_clr.RESET}")
    else:
        total = 0
        for idx, product_qty in enumerate(shopping_list, start=1):
            product_obj = product_qty[0]
            quantity = product_qty[1]
            product_name = product_obj.name
            unit_price = product_obj.price
            subtotal = unit_price * quantity
            print(
                f"{idx}. Product: {txt_clr.LY}{product_name}{txt_clr.RESET} "
                f"| Quantity {txt_clr.LB}{quantity}{txt_clr.RESET} "
                f"| Unit Price ${txt_clr.LG}{unit_price}{txt_clr.RESET} "
                f"| Subtotal ${txt_clr.G}{subtotal}{txt_clr.RESET}"
            )
            total += subtotal
        print(f"Current total ${txt_clr.LG}{total}{txt_clr.RESET}")
    print("_________________________________________________")


def make_an_order(store_obj):
    """
    Prompts the user to make an order, allowing them to add multiple items
    before completing the purchase. It uses a temporary stock to show live changes
    without modifying real store quantities until the order is finalized.
    """
    # Build a temp stock dictionary for normal products
    temp_stock = {}
    for p in store_obj.get_all_products():
        # Only track real quantity for normal, stocked products
        if not isinstance(p, (products.AddOns, products.NonStockedProduct)) and p.active:
            temp_stock[p] = p.quantity

    order_incomplete = True
    shopping_list = []
    shipping_added = False

    while order_incomplete:
        # Gather active products, ensuring AddOns and LimitedProduct are removed once added
        products_in_store = [
            p for p in get_all_products_in_store(store_obj)
            if not (
                # Exclude one-time purchase products if already in the shopping list
                (isinstance(p, (products.AddOns, products.LimitedProduct)) and any(
                    item[0] == p for item in shopping_list))
            )
        ]

        print(f"\n--------------------- {txt_clr.LW}Make an Order{txt_clr.RESET} -------------------")
        print("_______________________________________________________\n")

        # Display menu with the correct formatting
        for idx, product in enumerate(products_in_store, start=1):
            if isinstance(product, products.AddOns):
                print(
                    f"{idx}. Add On: {txt_clr.LY}{product.name}{txt_clr.RESET} "
                    f"| Price: ${txt_clr.LG}{product.price:.2f}{txt_clr.RESET} "
                    f"| {txt_clr.LC}One-time purchase per order{txt_clr.RESET}"
                )
            elif isinstance(product, products.LimitedProduct):
                print(
                    f"{idx}. Limited Product: {txt_clr.LY}{product.name}{txt_clr.RESET} "
                    f"| Price: ${txt_clr.LG}{product.price:.2f}{txt_clr.RESET} "
                    f"| Purchase Limit: {txt_clr.LC}{product.purchase_limit}{txt_clr.RESET}"
                )
            else:
                # Normal Products
                promo_str = f" | Promotion: {txt_clr.LR}{product.promotion.name}{txt_clr.RESET}" if product.promotion else ""
                print(
                    f"{idx}. Product: {txt_clr.LY}{product.name}{txt_clr.RESET} "
                    f"| Price: ${txt_clr.LG}{product.price:.2f}{txt_clr.RESET} "
                    f"| Quantity: {txt_clr.LB}{product.quantity}{txt_clr.RESET}{promo_str}"
                )

        menu_size = len(products_in_store)

        # Show "Show Cart" only if cart not empty
        show_cart_option = None
        if shopping_list:
            show_cart_option = menu_size + 1
            print(f"{show_cart_option}. {txt_clr.LC}Show Shopping Cart Contents{txt_clr.RESET}")
            menu_size += 1

        # Show "Complete Order" only if cart not empty
        complete_order_option = None
        if shopping_list:
            complete_order_option = menu_size + 1
            print(f"{complete_order_option}. {txt_clr.LB}Complete Current Order{txt_clr.RESET}")
            menu_size += 1

        # Always show "Exit Ordering Process"
        exit_option = menu_size + 1
        print(f"{exit_option}. {txt_clr.LR}Exit Ordering Process{txt_clr.RESET}")
        menu_size += 1

        print("_______________________________________________________")

        choice = get_valid_int_input("\nEnter a product number or action: ", 1, menu_size)

        # Handle "Exit Ordering Process" => cancel the order, do nothing to real stock
        if choice == exit_option:
            print(f"{txt_clr.LR}Order canceled. Returning to main menu...{txt_clr.RESET}")
            return None

        # Handle "Show Shopping Cart"
        if show_cart_option and choice == show_cart_option:
            show_shopping_cart(shopping_list)
            continue

        # Handle "Complete Order"
        if complete_order_option and choice == complete_order_option:
            order_incomplete = False
            break

        # User picked an actual product from the menu
        chosen_product = products_in_store[choice - 1]

        # If AddOn (one-time purchase, e.g., shipping, warranty, gift wrapping)
        if isinstance(chosen_product, products.AddOns):
            # Add shipping with quantity=1
            shopping_list.append((chosen_product, 1))
            shipping_added = True
            print(f"{txt_clr.LY}Shipping{txt_clr.RESET} added to shopping cart.")

            # Prompt if user wants more
            more_items = input("Do you want to add another item? (yes/no): ").strip().lower()
            if more_items not in {"y", "yes", "yeah", "yep", "yup"}:
                # Break the loop => proceed to shipping check
                break
            else:
                continue

        # If Limited Product
        if isinstance(chosen_product, products.LimitedProduct):
            order_quantity = get_valid_int_input(
                f"Enter quantity for {txt_clr.LY}{chosen_product.name}{txt_clr.RESET} "
                f"(Limit: {chosen_product.purchase_limit}): ", min_val=1, max_val=chosen_product.purchase_limit
            )
            shopping_list.append((chosen_product, order_quantity))
            print(f"{txt_clr.LY}{chosen_product.name}{txt_clr.RESET} "
                  f"| Quantity {txt_clr.LB}{order_quantity}{txt_clr.RESET} added to shopping cart.")

        # If Non-Stocked Product
        elif isinstance(chosen_product, products.NonStockedProduct):
            order_quantity = get_valid_int_input(
                f"Enter quantity for {txt_clr.LY}{chosen_product.name}{txt_clr.RESET}: ",
                min_val=1
            )
            # No stock limit to check, add directly
            shopping_list.append((chosen_product, order_quantity))
            print(f"{txt_clr.LY}{chosen_product.name}{txt_clr.RESET} x {order_quantity} added to cart.")

        else:
            # Normal (stocked) product => check the temp stock
            current_temp_qty = temp_stock[chosen_product]
            order_quantity = get_valid_int_input(
                f"Enter quantity for {txt_clr.LY}{chosen_product.name}{txt_clr.RESET}: ",
                min_val=1
            )

            if order_quantity <= current_temp_qty:
                # Deduct from temp stock
                temp_stock[chosen_product] = current_temp_qty - order_quantity
                shopping_list.append((chosen_product, order_quantity))
                print(f"{txt_clr.LY}{chosen_product.name}{txt_clr.RESET} "
                      f"| Quantity {txt_clr.LB}{order_quantity}{txt_clr.RESET} added to shopping cart.")
            else:
                print(f"Insufficient temp stock for {txt_clr.LR}{order_quantity}{txt_clr.RESET}. "
                      f"Only {txt_clr.LB}{current_temp_qty}{txt_clr.RESET} available.")
                continue

        # Ask if user wants more items
        more_items = input("Do you want to add another item? (yes/no): ").strip().lower()
        if more_items not in {"y", "yes", "yeah", "yep", "yup"}:
            break

    # After finishing or choosing "Complete Order", see if we need shipping
    if not shipping_added:
        # user might want shipping
        shopping_list, shipping_added = check_and_offer_shipping(shopping_list, shipping_added)

    # Now finalize the purchase => real store changes happen here
    try:
        total_price = store_obj.order(shopping_list)
        print(f"Order successful! Total cost: ${txt_clr.LG}{total_price:.2f}{txt_clr.RESET}")
    except Exception as e:
        print(f"Order failed: {str(e)}")


def check_and_offer_shipping(shopping_list, shipping_already_added):
    """
    Ensures that shipping is only added if required and not already present.
    Called only at the end, if shipping wasn't already added.
    """
    if shipping_already_added:
        return shopping_list, shipping_already_added

    has_physical_products = any(
        isinstance(item[0], products.Product)
        and not isinstance(item[0], products.NonStockedProduct)
        for item in shopping_list
    )

    if has_physical_products:
        need_shipping = input("Do you need shipping? (yes/no): ").strip().lower()
        if need_shipping in {"y", "yes"}:
            shipping_item = products.AddOns("Standard Shipping", price=10)
            shopping_list.append((shipping_item, 1))
            print(f"{txt_clr.LY}Shipping{txt_clr.RESET} added to shopping cart.")
            shipping_already_added = True

    return shopping_list, shipping_already_added


def main():
    # Setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=650),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.Product("Sony WH-1000XM5", price=350, quantity=300),
        products.Product("iPad Pro", price=1200, quantity=150),
        products.Product("Dell XPS 13", price=1400, quantity=200),
        products.NonStockedProduct("Windows License", price=125),
        products.NonStockedProduct("Adobe Photoshop Subscription", price=20),
        products.LimitedProduct("Best Buy Limited Edition Mouse Mat", price=10, quantity=500, purchase_limit=1),
        products.LimitedProduct("Best Buy Coffee Cup", price=5, quantity=200, purchase_limit=1),
        products.AddOns("Extended Warranty", price=100),
        products.AddOns("Gift Wrapping", price=5),
        products.AddOns("Standard Shipping", price=10)
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

    print(f"------------- {txt_clr.LW}Welcome to the Best Buy Store!{txt_clr.RESET} -------------")

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
