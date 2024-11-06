class InsufficientStockError(Exception):
    """Exception raised when there is not enough stock for a product."""
    pass


class ProductNotFoundError(Exception):
    """Exception raised when a product is not found."""
    pass


class OrderNotFoundError(Exception):
    """Exception raised when an order is not found."""
    pass
