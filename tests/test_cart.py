import pytest
from shop.product import Product
from shop.cart import ShoppingCart


def test_new_cart_is_empty():
    cart = ShoppingCart()
    assert cart.is_empty() is True
    assert cart.get_item_count() == 0
    assert cart.get_total() == 0


def test_add_single_product():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    cart.add_product(keyboard)
    assert cart.is_empty() is False
    assert cart.get_item_count() == 1


def test_add_two_different_products():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    mouse = Product("Mouse", 500)
    cart.add_product(keyboard)
    cart.add_product(mouse)
    assert cart.get_item_count() == 2
    assert len(cart.get_items()) == 2


def test_add_same_product_twice_increases_quantity():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    cart.add_product(keyboard, 2)
    cart.add_product(keyboard, 3)
    assert cart.get_item_count() == 5
    assert cart.get_items()[keyboard] == 5


def test_get_total_calculates_sum_correctly():
    cart = ShoppingCart()
    cart.add_product(Product("Keyboard", 1000))
    cart.add_product(Product("Mouse", 500))
    assert cart.get_total() == 1500.0


def test_get_total_with_quantity_greater_than_one():
    cart = ShoppingCart()
    cart.add_product(Product("Keyboard", 1000), 3)
    assert cart.get_total() == 3000.0


def test_remove_product_completely():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    cart.add_product(keyboard, 2)
    cart.remove_product(keyboard)
    assert cart.is_empty() is True


def test_remove_product_partially():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    cart.add_product(keyboard, 5)
    cart.remove_product(keyboard, 2)
    assert cart.get_item_count() == 3


def test_remove_more_than_in_cart_raises_error():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    cart.add_product(keyboard, 2)
    with pytest.raises(ValueError, match="Cannot remove more than in cart"):
        cart.remove_product(keyboard, 3)


def test_remove_missing_product_raises_error():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    with pytest.raises(ValueError, match="Product is not in cart"):
        cart.remove_product(keyboard)


def test_get_item_count_returns_total_units():
    cart = ShoppingCart()
    cart.add_product(Product("Keyboard", 1000), 2)
    cart.add_product(Product("Mouse", 500), 4)
    assert cart.get_item_count() == 6


def test_clear_empties_cart():
    cart = ShoppingCart()
    cart.add_product(Product("Keyboard", 1000), 2)
    cart.clear()
    assert cart.is_empty() is True
    assert cart.get_item_count() == 0


@pytest.mark.parametrize("bad_qty", [0, -1, 1.5])
def test_add_invalid_quantity_raises_error(bad_qty):
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        cart.add_product(keyboard, bad_qty)


def test_apply_10_percent_coupon():
    cart = ShoppingCart()
    cart.add_product(Product("Keyboard", 1000), 2)
    cart.set_coupon(10)
    assert cart.get_total() == 1800.0


def test_coupon_above_20_raises_error():
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="Coupon must be between 0 and 20"):
        cart.set_coupon(25)


def test_total_with_product_discount():
    cart = ShoppingCart()
    monitor = Product("Monitor", 10000, discount_percent=10)
    cart.add_product(monitor, 2)
    assert cart.get_total() == 18000.0


def test_total_with_product_discount_and_coupon():
    cart = ShoppingCart()
    monitor = Product("Monitor", 10000, discount_percent=10)
    cart.add_product(monitor, 2)
    cart.set_coupon(10)
    assert cart.get_total() == 16200.0


def test_clear_resets_coupon():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    cart.add_product(keyboard, 1)
    cart.set_coupon(15)
    cart.clear()
    cart.add_product(keyboard, 1)
    assert cart.get_total() == 1000.0


def test_get_items_returns_copy():
    cart = ShoppingCart()
    keyboard = Product("Keyboard", 1000)
    cart.add_product(keyboard, 1)
    items_copy = cart.get_items()
    items_copy[keyboard] = 99
    assert cart.get_items()[keyboard] == 1