from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # Import CORS
import json
import os


app = Flask(__name__)
CORS ( app )


def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)['products']
    
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
    new_products = request.json
    products = load_products()
    new_products['id'] = len(products) + 1
    products.append(new_products)
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(new_products), 201

@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

if __name__ == '__main__':
    app.run(debug=True)
