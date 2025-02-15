import pytest
from products import Product
from promotions import PercentageDiscount, SecondItemHalfPrice, BuyTwoGetOneFree


def test_percentage_discount():
    """Test applying a percentage discount to a product."""
    product = Product("Laptop", 1000, 10, PercentageDiscount("20% Off", 20))
    assert product.buy(1) == 800  # 20% off 1000


def test_second_item_half_price():
    """Test applying second item at half price discount."""
    product = Product("Headphones", 200, 10, SecondItemHalfPrice("Second Item Half Price"))
    assert product.buy(1) == 200  # No discount for one item
    assert product.buy(2) == 300  # First item full price, second half price
    assert product.buy(3) == 500  # 2 full price + 1 half price


def test_buy_two_get_one_free():
    """Test applying buy 2, get 1 free promotion."""
    # Test with fresh instances to prevent stock depletion
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(1) == 50  # No discount for one item
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(2) == 100  # No discount for two items
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(3) == 100  # Pay for 2, get 1 free
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(4) == 150  # Pay for 3, get 1 free
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(6) == 200  # Pay for 4, get 2 free
