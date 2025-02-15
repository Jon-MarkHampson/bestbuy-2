import pytest
from products import Product


def test_product_instance_creation():
    """Test that creating a normal product works"""
    product_instance = Product("MacBook Air M2", price=1450, quantity=100)
    assert product_instance.name == "MacBook Air M2"
    assert product_instance.price == 1450
    assert product_instance.quantity == 100
    assert product_instance.active is True


def test_invalid_product_creation():
    """Test that creating a product with invalid details raises an exception."""
    with pytest.raises(ValueError, match="The name cannot be empty"):
        Product("", price=1450, quantity=100)

    with pytest.raises(ValueError, match="The price must be a non-negative value"):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_instance_deactivates_when_empty():
    """Test that when a product reaches 0 quantity, it becomes inactive."""
    product_instance = Product("MacBook Air M2", price=1450, quantity=10)
    product_instance.set_quantity(0)
    assert product_instance.active is False


def test_product_instance_purchase_modifies_quantity():
    """Test that product purchase modifies the quantity and returns the right output."""
    product_instance = Product("MacBook Air M2", price=1450, quantity=10)
    product_instance.buy(5)
    assert product_instance.quantity == 5


def test_buying_zero_quantity_raises_exception():
    """Test that buying a zero quantity than exists raises an exception."""
    product_instance = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError, match="The quantity to buy must be greater than 0."):
        product_instance.buy(0)


def test_buying_more_than_available_raises_exception():
    """Test that buying a larger quantity than exists raises an exception."""
    product_instance = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError, match=f"Insufficient stock to complete the purchase. Available: {product_instance.quantity}"):
        product_instance.buy(6)