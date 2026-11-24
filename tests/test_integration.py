import pytest
from shop.product import Product
from shop.cart import ShoppingCart
from shop.inventory import Inventory
from shop.order_service import OrderService


def test_scenario_1_successful_order_creation():
    laptop = Product("Laptop", 30000)
    inventory = Inventory()
    inventory.add_product(laptop, 5)
    cart = ShoppingCart()
    cart.add_product(laptop, 2)
    service = OrderService(inventory)

    order = service.create_order(cart)

    assert order["status"] == "created"
    assert order["total"] == 60000
    assert inventory.get_quantity(laptop) == 3
    assert cart.is_empty() is True
    assert service.get_order_count() == 1


def test_scenario_2_insufficient_stock_prevents_order():
    laptop = Product("Laptop", 30000)
    inventory = Inventory()
    inventory.add_product(laptop, 2)
    cart = ShoppingCart()
    cart.add_product(laptop, 3)
    service = OrderService(inventory)

    with pytest.raises(ValueError, match="Not enough stock for Laptop"):
        service.create_order(cart)

    assert inventory.get_quantity(laptop) == 2
    assert cart.get_item_count() == 3
    assert service.get_order_count() == 0


def test_scenario_3_order_with_multiple_products():
    keyboard = Product("Keyboard", 1000)
    mouse = Product("Mouse", 500)
    inventory = Inventory()
    inventory.add_product(keyboard, 10)
    inventory.add_product(mouse, 10)
    cart = ShoppingCart()
    cart.add_product(keyboard, 2)
    cart.add_product(mouse, 1)
    service = OrderService(inventory)

    order = service.create_order(cart)

    assert order["total"] == 2500
    assert order["status"] == "created"
    assert inventory.get_quantity(keyboard) == 8
    assert inventory.get_quantity(mouse) == 9
    assert cart.is_empty() is True


def test_scenario_4_empty_cart_raises_error():
    inventory = Inventory()
    cart = ShoppingCart()
    service = OrderService(inventory)

    with pytest.raises(ValueError, match="Cart is empty"):
        service.create_order(cart)

    assert service.get_order_count() == 0


def test_scenario_5_order_with_product_discount_and_cart_coupon():
    monitor = Product("Monitor", 10000, discount_percent=10)
    inventory = Inventory()
    inventory.add_product(monitor, 5)
    cart = ShoppingCart()
    cart.add_product(monitor, 2)
    cart.set_coupon(10)
    service = OrderService(inventory)

    order = service.create_order(cart)

    assert order["status"] == "created"
    assert order["total"] == 16200
    assert inventory.get_quantity(monitor) == 3
    assert cart.is_empty() is True
    cart.add_product(monitor, 1)
    assert cart.get_total() == 9000


def test_scenario_6_insufficient_one_of_several_products_keeps_stock_intact():
    keyboard = Product("Keyboard", 1000)
    mouse = Product("Mouse", 500)
    inventory = Inventory()
    inventory.add_product(keyboard, 5)
    inventory.add_product(mouse, 1)
    cart = ShoppingCart()
    cart.add_product(keyboard, 2)
    cart.add_product(mouse, 3)
    service = OrderService(inventory)

    with pytest.raises(ValueError, match="Not enough stock for Mouse"):
        service.create_order(cart)

    assert inventory.get_quantity(keyboard) == 5
    assert inventory.get_quantity(mouse) == 1
    assert cart.get_item_count() == 5
    assert service.get_order_count() == 0


def test_scenario_7_cart_and_coupon_cleared_after_order():
    keyboard = Product("Keyboard", 1000)
    inventory = Inventory()
    inventory.add_product(keyboard, 10)
    cart = ShoppingCart()
    cart.add_product(keyboard, 3)
    cart.set_coupon(10)
    service = OrderService(inventory)

    service.create_order(cart)

    assert inventory.get_quantity(keyboard) == 7
    assert cart.is_empty() is True
    assert cart.get_item_count() == 0
    assert cart.get_total() == 0
    cart.add_product(keyboard, 1)
    assert cart.get_total() == 1000


def test_scenario_8_order_history_and_lookup():
    keyboard = Product("Keyboard", 1000)
    mouse = Product("Mouse", 500)
    inventory = Inventory()
    inventory.add_product(keyboard, 10)
    inventory.add_product(mouse, 10)
    service = OrderService(inventory)

    cart1 = ShoppingCart()
    cart1.add_product(keyboard, 2)
    order1 = service.create_order(cart1)

    cart2 = ShoppingCart()
    cart2.add_product(mouse, 3)
    order2 = service.create_order(cart2)

    assert order1["status"] == "created"
    assert order2["status"] == "created"
    assert order1["id"] != order2["id"]
    assert service.get_order_count() == 2
    assert service.get_order(order1["id"])["total"] == 2000
    assert service.get_order(order2["id"])["total"] == 1500
    assert inventory.get_quantity(keyboard) == 8
    assert inventory.get_quantity(mouse) == 7

    with pytest.raises(ValueError, match="Order not found"):
        service.get_order(999)