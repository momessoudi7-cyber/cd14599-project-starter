# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders', 'delete_order']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage

    def add_order(self, order_id: str, item_name: str, quantity: int,
                  customer_id: str, status: str = "pending"):
        """
        Add a new order to the system.

        Args:
            order_id (str): Unique identifier for the order.
            item_name (str): Name of the item being ordered (cannot be empty or whitespace).
            quantity (int): Quantity of the item (must be positive integer).
            customer_id (str): Identifier for the customer (cannot be empty or whitespace).
            status (str, optional): Status of the order. Defaults to "pending".

        Raises:
            ValueError: If validations fail (quantity, uniqueness, empty fields).

        Returns:
            None
        """
        # Validate item_name
        if not item_name or not item_name.strip():
            raise ValueError("Item name cannot be empty or whitespace.")

        # Validate customer_id
        if not customer_id or not customer_id.strip():
            raise ValueError("Customer ID cannot be empty or whitespace.")

        # Validate quantity
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        # Validate order_id uniqueness
        if self.storage.get_order(order_id) is not None:
            raise ValueError("Order ID must be unique.")

        # Create order dictionary
        order = {
            'order_id': order_id,
            'item_name': item_name,
            'quantity': quantity,
            'customer_id': customer_id,
            'status': status
        }

        # Save the order using storage
        self.storage.save_order(order_id, order)

    def get_order_by_id(self, order_id: str):
        """
        Retrieve an order by its ID.

        Args:
            order_id (str): The unique identifier of the order.

        Returns:
            dict or None: The order dictionary if found, otherwise None.
        """
        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):
        """
        Update the status of an existing order.

        Args:
            order_id (str): The unique identifier of the order.
            new_status (str): The new status to set for the order.

        Raises:
            ValueError: If the order with the given ID does not exist.

        Returns:
            None
        """
        order = self.storage.get_order(order_id)
        if order is None:
            raise ValueError(f"Order with ID {order_id} not found.")
        order['status'] = new_status
        self.storage.save_order(order_id, order)

    def list_all_orders(self):
        """
        Retrieve a list of all orders.

        Returns:
            list: A list of all order dictionaries.
        """
        return list(self.storage.get_all_orders().values())

    def list_orders_by_status(self, status: str):
        """
        Retrieve a list of orders filtered by status.

        Args:
            status (str): The status to filter orders by.

        Returns:
            list: A list of order dictionaries with the matching status.
        """
        all_orders = self.storage.get_all_orders()
        return [order for order in all_orders.values()
                if order['status'] == status]

    def delete_order(self, order_id: str):
        """
        Delete an order by its ID.

        Args:
            order_id (str): The unique identifier of the order to delete.

        Raises:
            ValueError: If the order with the given ID does not exist.

        Returns:
            None
        """
        if self.storage.get_order(order_id) is None:
            raise ValueError(f"Order with ID {order_id} not found.")
        self.storage.delete_order(order_id)
