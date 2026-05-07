from flask import Flask, request, jsonify, send_from_directory
from backend.order_tracker import OrderTracker
from backend.in_memory_storage import InMemoryStorage

app = Flask(__name__, static_folder='../frontend')
in_memory_storage = InMemoryStorage()
order_tracker = OrderTracker(in_memory_storage)

@app.route('/')
def serve_index():
    """
    Serve the main index.html file.

    Returns:
        Response: The index.html file.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """
    Serve static files from the frontend directory.

    Args:
        filename (str): The path to the static file.

    Returns:
        Response: The requested static file.
    """
    return send_from_directory(app.static_folder, filename)

@app.route('/api/orders', methods=['POST'])
def add_order_api():
    """
    Add a new order via API.

    Returns:
        Response: JSON of the created order with 201, or error with 400.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        order_id = data.get('order_id')
        item_name = data.get('item_name')
        quantity = data.get('quantity')
        customer_id = data.get('customer_id')
        status = data.get('status', 'pending')

        order_tracker.add_order(order_id, item_name, quantity,
                                customer_id, status)

        # Retrieve the created order
        created_order = order_tracker.get_order_by_id(order_id)
        return jsonify(created_order), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/orders/<string:order_id>', methods=['GET'])
def get_order_api(order_id):
    """
    Retrieve a single order by its ID.

    Args:
        order_id (str): The unique identifier of the order.

    Returns:
        Response: JSON of the order with 200, or error with 404 if not found.
    """
    order = order_tracker.get_order_by_id(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200

@app.route('/api/orders/<string:order_id>/status', methods=['PUT'])
def update_order_status_api(order_id):
    """
    Update the status of an order.

    Args:
        order_id (str): The unique identifier of the order.

    Returns:
        Response: JSON of the updated order with 200, or error with 400/404.
    """
    data = request.get_json()
    if not data or 'new_status' not in data:
        return jsonify({"error": "new_status is required"}), 400

    try:
        new_status = data['new_status']
        order_tracker.update_order_status(order_id, new_status)
        updated_order = order_tracker.get_order_by_id(order_id)
        return jsonify(updated_order), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/orders', methods=['GET'])
def list_orders_api():
    """
    List all orders or filter by status.

    Query Params:
        status (str, optional): Filter orders by this status.

    Returns:
        Response: JSON list of orders with 200.
    """
    status = request.args.get('status')
    if status:
        orders = order_tracker.list_orders_by_status(status)
    else:
        orders = order_tracker.list_all_orders()
    return jsonify(orders), 200

@app.route('/api/orders/<string:order_id>', methods=['DELETE'])
def delete_order_api(order_id):
    """
    Delete an order by its ID.

    Args:
        order_id (str): The unique identifier of the order.

    Returns:
        Response: 204 No Content on success, or error with 404.
    """
    try:
        order_tracker.delete_order(order_id)
        return '', 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
