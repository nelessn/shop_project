import pytest
from shop.product import Product
from shop.inventory import Inventory


def test_add_new_product_to_inventory():
    inv = Inventory()
    keyboard = Product("Keyboard", 1000)
    inv.add_product(keyboard, 10)
    assert inv.get_quantity(keyboard) == 10


def test_add_existing_product_increases_stock():
    inv = Inventory()
    keyboard = Product("Keyboard", 1000)
    inv.add_product(keyboard, 5)
    inv.add_product(keyboard, 7)
    assert inv.get_quantity(keyboard) == 12


def test_get_quantity_returns_exact_stock():
    inv = Inventory()
    mouse = Product("Mouse", 500)
    inv.add_product(mouse, 4)
    assert inv.get_quantity(mouse) == 4


def test_is_available_returns_true_when_enough_stock():
    inv = Inventory()
    mouse = Product("Mouse", 500)
    inv.add_product(mouse, 5)
    assert inv.is_available(mouse, 5) is True
    assert inv.is_available(mouse, 3) is True


def test_is_available_returns_false_when_not_enough_stock():
    inv = Inventory()
    mouse = Product("Mouse", 500)
    inv.add_product(mouse, 2)
    assert inv.is_available(mouse, 3) is False


def test_remove_product_decreases_stock():
    inv = Inventory()
    mouse = Product("Mouse", 500)
    inv.add_product(mouse, 10)
    inv.remove_product(mouse, 4)
    assert inv.get_quantity(mouse) == 6


def test_remove_more_than_available_raises_error():
    inv = Inventory()
    mouse = Product("Mouse", 500)
    inv.add_product(mouse, 3)
    with pytest.raises(ValueError, match="Not enough stock"):
        inv.remove_product(mouse, 5)


def test_missing_product_has_zero_quantity():
    inv = Inventory()
    laptop = Product("Laptop", 30000)
    assert inv.get_quantity(laptop) == 0


def test_add_zero_quantity_raises_error():
    inv = Inventory()
    laptop = Product("Laptop", 30000)
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        inv.add_product(laptop, 0)


def test_remove_negative_quantity_raises_error():
    inv = Inventory()
    laptop = Product("Laptop", 30000)
    inv.add_product(laptop, 5)
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        inv.remove_product(laptop, -2)


def test_custom_low_stock_limit():
    inv = Inventory(low_stock_limit=5)
    assert inv.low_stock_limit == 5


def test_negative_low_stock_limit_raises_error():
    with pytest.raises(ValueError, match="Low stock limit cannot be negative"):
        Inventory(low_stock_limit=-1)


def test_get_low_stock_products_returns_scarce_items():
    inv = Inventory(low_stock_limit=3)
    p1 = Product("Keyboard", 1000)
    p2 = Product("Mouse", 500)
    inv.add_product(p1, 2)
    inv.add_product(p2, 10)
    assert inv.get_low_stock_products() == [p1]


def test_product_at_exact_low_stock_limit_is_included():
    inv = Inventory(low_stock_limit=3)
    p1 = Product("Keyboard", 1000)
    inv.add_product(p1, 3)
    assert p1 in inv.get_low_stock_products()


def test_product_above_low_stock_limit_is_excluded():
    inv = Inventory(low_stock_limit=3)
    p1 = Product("Keyboard", 1000)
    inv.add_product(p1, 4)
    assert p1 not in inv.get_low_stock_products()


def test_remove_last_unit_leaves_zero_stock():
    inv = Inventory()
    p1 = Product("Keyboard", 1000)
    inv.add_product(p1, 1)
    inv.remove_product(p1, 1)
    assert inv.get_quantity(p1) == 0