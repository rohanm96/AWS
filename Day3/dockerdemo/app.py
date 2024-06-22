from flask import Flask, request, jsonify
app = Flask(__name__)
products = []

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/welcome')
def welcome():
    return 'Welcome'


@app.route('/product', methods=['POST'])
def add_product():
    product_data = request.get_json()

    # Validate the product data
    if not all(key in product_data for key in ('code', 'name', 'description', 'supplier', 'price')):
        return jsonify({'message': 'Missing product data'}), 400

    products.append(product_data)
    return jsonify({'message': 'Product added successfully!'}), 201

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': products}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')