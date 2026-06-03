from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample internal memory list updated with deadlines
items = [
    {"id": 1, "name": "Learn Python & Flask", "deadline": "2026-06-10"},
    {"id": 2, "name": "Build a CRUD app", "deadline": "2026-06-15"}
]

@app.route('/')
def home():
    return app.send_static_file('index.html')

# 1. READ
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items)

# 2. CREATE
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name field is required"}), 400
    
    new_id = items[-1]['id'] + 1 if items else 1
    new_item = {
        "id": new_id, 
        "name": data['name'],
        "deadline": data.get('deadline', '')  # Accept deadline string
    }
    items.append(new_item)
    return jsonify(new_item), 201

# 3. UPDATE
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    for item in items:
        if item['id'] == item_id:
            item['name'] = data.get('name', item['name'])
            item['deadline'] = data.get('deadline', item['deadline']) # Update deadline
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# 4. DELETE
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    initial_length = len(items)
    items = [item for item in items if item['id'] != item_id]
    if len(items) < initial_length:
        return jsonify({"message": f"Item {item_id} deleted successfully"})
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)