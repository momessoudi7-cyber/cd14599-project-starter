import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---

def test_add_order_success(order_tracker, mock_storage):
    """Test successful addition of a valid order."""
    order_tracker.add_order("order1", "item1", 5, "cust1")

    # Check that save_order was called with the correct dict
    mock_storage.save_order.assert_called_once_with("order1", {
        'order_id': "order1",
        'item_name': "item1",
        'quantity': 5,
        'customer_id': "cust1",
        'status': "pending"
    })

def test_add_order_duplicate_id(order_tracker, mock_storage):
    """Test ValueError for duplicate order_id."""
    # Mock get_order to return an existing order
    mock_storage.get_order.return_value = {'order_id': "order1"}

    with pytest.raises(ValueError, match="Order ID must be unique"):
        order_tracker.add_order("order1", "item1", 5, "cust1")

def test_add_order_invalid_quantity_zero(order_tracker, mock_storage):
    """Test ValueError for quantity <= 0."""
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        order_tracker.add_order("order1", "item1", 0, "cust1")

def test_add_order_invalid_quantity_negative(order_tracker, mock_storage):
    """Test ValueError for negative quantity."""
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        order_tracker.add_order("order1", "item1", -1, "cust1")

def test_add_order_invalid_quantity_not_int(order_tracker, mock_storage):
    """Test ValueError for quantity not an integer."""
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        order_tracker.add_order("order1", "item1", 5.5, "cust1")

def test_add_order_invalid_item_name_empty(order_tracker, mock_storage):
    """Test ValueError for empty item_name."""
    with pytest.raises(ValueError, match="Item name cannot be empty or whitespace"):
        order_tracker.add_order("order1", "", 5, "cust1")

def test_add_order_invalid_item_name_whitespace(order_tracker, mock_storage):
    """Test ValueError for whitespace-only item_name."""
    with pytest.raises(ValueError, match="Item name cannot be empty or whitespace"):
        order_tracker.add_order("order1", "   ", 5, "cust1")

def test_add_order_invalid_customer_id_empty(order_tracker, mock_storage):
    """Test ValueError for empty customer_id."""
    with pytest.raises(ValueError, match="Customer ID cannot be empty or whitespace"):
        order_tracker.add_order("order1", "item1", 5, "")

def test_add_order_invalid_customer_id_whitespace(order_tracker, mock_storage):
    """Test ValueError for whitespace-only customer_id."""
    with pytest.raises(ValueError, match="Customer ID cannot be empty or whitespace"):
        order_tracker.add_order("order1", "item1", 5, "   ")

def test_get_order_by_id(order_tracker, mock_storage):
    """Test get_order_by_id returns the order from storage."""
    mock_order = {'order_id': 'order1', 'status': 'pending'}
    mock_storage.get_order.return_value = mock_order

    result = order_tracker.get_order_by_id('order1')
    assert result == mock_order
    mock_storage.get_order.assert_called_once_with('order1')

def test_get_order_by_id_not_found(order_tracker, mock_storage):
    """Test get_order_by_id returns None if not found."""
    mock_storage.get_order.return_value = None

    result = order_tracker.get_order_by_id('nonexistent')
    assert result is None

def test_list_all_orders(order_tracker, mock_storage):
    """Test list_all_orders returns all orders as a list."""
    mock_orders = {
        'order1': {'order_id': 'order1', 'status': 'pending'},
        'order2': {'order_id': 'order2', 'status': 'shipped'}
    }
    mock_storage.get_all_orders.return_value = mock_orders

    result = order_tracker.list_all_orders()
    assert result == list(mock_orders.values())

def test_list_orders_by_status(order_tracker, mock_storage):
    """Test list_orders_by_status filters by exact status."""
    mock_orders = {
        'order1': {'order_id': 'order1', 'status': 'pending'},
        'order2': {'order_id': 'order2', 'status': 'shipped'},
        'order3': {'order_id': 'order3', 'status': 'pending'}
    }
    mock_storage.get_all_orders.return_value = mock_orders

    result = order_tracker.list_orders_by_status('pending')
    expected = [mock_orders['order1'], mock_orders['order3']]
    assert result == expected

def test_update_order_status_success(order_tracker, mock_storage):
    """Test successful update of order status."""
    mock_order = {'order_id': 'order1', 'status': 'pending'}
    mock_storage.get_order.return_value = mock_order

    order_tracker.update_order_status('order1', 'shipped')

    # Check that save_order was called with updated order
    expected_order = {'order_id': 'order1', 'status': 'shipped'}
    mock_storage.save_order.assert_called_once_with('order1', expected_order)

def test_update_order_status_not_found(order_tracker, mock_storage):
    """Test ValueError when order not found."""
    mock_storage.get_order.return_value = None

    with pytest.raises(ValueError, match="Order with ID nonexistent not found"):
        order_tracker.update_order_status('nonexistent', 'shipped')

def test_delete_order_success(order_tracker, mock_storage):
    """Test successful deletion of an order."""
    mock_order = {'order_id': 'order1', 'status': 'pending'}
    mock_storage.get_order.return_value = mock_order
    
    order_tracker.delete_order('order1')
    
    mock_storage.delete_order.assert_called_once_with('order1')

def test_delete_order_not_found(order_tracker, mock_storage):
    """Test ValueError when trying to delete non-existent order."""
    mock_storage.get_order.return_value = None
    
    with pytest.raises(ValueError, match="Order with ID nonexistent not found"):
        order_tracker.delete_order('nonexistent')
#
