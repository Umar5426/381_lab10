from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # Import CORS
import json
import os


app = Flask(__name__)
CORS ( app )


def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)['products']

def save_products(products):
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)

@app.route('/products', methods=['GET'])
@app.route('/products/<int:products_id>', methods=['GET'])  
def get_products(products_id=None):
    products = load_products()
    if products_id is None:
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == products_id), None)
        return jsonify(product) if product else ('', 404)

@app.route('/products/add', methods=['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    save_products(products)
    return jsonify(new_product), 201

@app.route('/products/update/<int:products_id>', methods=['PUT'])
def update_product(products_id):
    updated_product = request.json
    products = load_products()
    for product in products:
        if product['id'] == products_id:
            product.update(updated_product)
            save_products(products)
            return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/products/remove/<int:products_id>', methods=['DELETE'])
def remove_product(products_id):
    products = load_products()
    for product in products:
        if product['id'] == products_id:
            products.remove(product)
            save_products(products)
            return jsonify({"message": "Product removed successfully"}), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

if __name__ == '__main__':
    app.run(debug=True)
