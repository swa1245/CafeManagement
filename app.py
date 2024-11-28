from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

try:
    with open('menu.json', 'r') as file:
        data = json.load(file)
        items = data.get('items', [])
        reviews = data.get('reviews', [])
except FileNotFoundError:
    items = []
    reviews = []

order_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({'menu': items})

@app.route('/menu', methods=['POST'])
def add_item():
    new_item = request.json
    items.append(new_item)
    save_data()
    return jsonify({'message': 'Item added successfully!', 'menu': items}), 201

@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_data = request.json
    for item in items:
        if item['id'] == item_id:
            item.update(updated_data)
            save_data()
            return jsonify({'message': 'Item updated successfully!', 'menu': items}), 200
    return jsonify({'message': 'Item not found!'}), 404

@app.route("/confirm-order", methods=["POST"])
def confirm_order():
    data = request.get_json()
    total_amount = data["total_amount"]
    order_history.append({
        "order_details": data.get("order_details", []),
        "total_amount": total_amount
    })
    return jsonify({"message": "Order confirmed!", "total_amount": total_amount})

@app.route('/order', methods=['POST'])
def order_food():
    order_ids = request.json.get('order_ids', [])
    order_details = [item for item in items if item['id'] in order_ids]
    total_amount = sum(float(item['price']) for item in order_details)
    return jsonify({'order_details': order_details, 'total_amount': total_amount})

@app.route('/order-history', methods=['GET'])
def get_order_history():
    return jsonify({'order_history': order_history})

def save_data():
   
    with open('menu.json', 'w') as file:
        json.dump({"items": items, "reviews": reviews}, file)

if __name__ == '__main__':
    app.run(debug=True)
