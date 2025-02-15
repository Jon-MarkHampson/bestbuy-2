import pytest
from products import Product
from promotions import PercentageDiscount, SecondItemHalfPrice, BuyTwoGetOneFree


def test_percentage_discount():
    """Test applying a percentage discount to a product."""
    product = Product("Laptop", 1000, 10, PercentageDiscount("20% Off", 20))
    assert product.buy(1) == 800  # 20% off 1000


def test_percentage_discount_invalid():
    """Test invalid percentage discount values."""
    with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100."):
        PercentageDiscount("Invalid Discount", -10)
    with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100."):
        PercentageDiscount("Invalid Discount", 150)


def test_second_item_half_price():
    """Test applying second item at half price discount."""
    product = Product("Headphones", 200, 10, SecondItemHalfPrice("Second Item Half Price"))
    assert product.buy(1) == 200  # No discount for one item
    assert product.buy(2) == 300  # First item full price, second half price
    assert product.buy(3) == 500  # 2 full price + 1 half price


def test_second_item_half_price_invalid():
    """Test invalid quantity for second item half price promotion."""
    product = Product("Headphones", 200, 10, SecondItemHalfPrice("Second Item Half Price"))
    with pytest.raises(ValueError, match="The quantity to buy must be greater than 0."):
        product.buy(0)



def test_buy_two_get_one_free():
    """Test applying buy 2, get 1 free promotion."""
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(1) == 50
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(2) == 100
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(3) == 100
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(4) == 150
    assert Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free")).buy(6) == 200


def test_buy_two_get_one_free_invalid():
    """Test invalid quantity for buy 2, get 1 free promotion."""
    product = Product("USB Cable", 50, 10, BuyTwoGetOneFree("Buy 2 Get 1 Free"))
    with pytest.raises(ValueError, match="The quantity to buy must be greater than 0."):
        product.buy(0)
