import pytest
from shop.product import Product


def test_product_is_created_with_name_price_and_category():
    product = Product("Keyboard", 1000, "Peripherals")
    assert product.name == "Keyboard"
    assert product.price == 5000
    assert product.category == "Peripherals"


def test_empty_product_name_raises_error():
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product("", 1000)


def test_whitespace_product_name_raises_error():
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        Product("   ", 1000)


def test_zero_price_raises_error():
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        Product("Keyboard", 0)


def test_negative_price_raises_error():
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        Product("Keyboard", -500)


def test_empty_category_raises_error():
    with pytest.raises(ValueError, match="Category cannot be empty"):
        Product("Keyboard", 1000, "   ")


def test_set_discount_10_percent_changes_final_price():
    product = Product("Keyboard", 1000)
    product.set_discount(10)
    assert product.get_final_price() == 900.0


def test_get_final_price_calculates_discount_correctly():
    product = Product("Mouse", 500, discount_percent=25)
    assert product.get_final_price() == 375.0


def test_zero_discount_leaves_price_unchanged():
    product = Product("Monitor", 8000, discount_percent=0)
    assert product.get_final_price() == 8000.0


def test_discount_above_50_raises_error():
    product = Product("Keyboard", 1000)
    with pytest.raises(ValueError, match="Discount must be between 0 and 50"):
        product.set_discount(51)


def test_negative_discount_raises_error():
    product = Product("Keyboard", 1000)
    with pytest.raises(ValueError, match="Discount must be between 0 and 50"):
        product.set_discount(-5)


def test_is_in_category_returns_true_for_matching_category():
    product = Product("Keyboard", 1000, "Electronics")
    assert product.is_in_category("Electronics") is True
    assert product.is_in_category("Furniture") is False


def test_is_in_category_is_case_insensitive():
    product = Product("Keyboard", 1000, "Electronics")
    assert product.is_in_category("electronics") is True
    assert product.is_in_category("  ELECTRONICS  ") is True