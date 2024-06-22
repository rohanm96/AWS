from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
products = []

# Database connection
connection = pymysql.connect(
    host='devopsdemodb.cdgcwgoq6pwq.ap-south-1.rds.amazonaws.com',
    user='admin',
    password='root1234',
    db='demo',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/welcome')
def welcome():
    return 'Welcome'


@app.route('/product', methods=['POST'])
def add_product():
    product_data = request.get_json()
    print("product data::",product_data)

    # Validate the product data
    if not all(key in product_data for key in ('name', 'description', 'supplier', 'price')):
        return jsonify({'message': 'Missing product data'}), 400

    #products.append(product_data)
    #return jsonify({'message': 'Product added successfully!'}), 201
    # Save product data to the database
    with connection.cursor() as cursor:
        sql = "INSERT INTO products (name,description,supplier,price) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (product_data['name'], product_data['description'], product_data['supplier'], int(product_data['price'])))
    connection.commit()
    return jsonify({'message': 'Product added successfully!'}), 201

@app.route('/products', methods=['GET'])
def get_products():
    #return jsonify({'products': products}), 200
    with connection.cursor() as cursor:
        sql = "SELECT * FROM products"
        cursor.execute(sql)
        result = cursor.fetchall()
    return jsonify({'products': result}), 200

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product_data = request.get_json()

    # Validate the product data
    if not all(key in product_data for key in ('code', 'name', 'description', 'supplier', 'price')):
        return jsonify({'message': 'Missing product data'}), 400

    # Update product data in the database
    with connection.cursor() as cursor:
        sql = "UPDATE products SET code = %s, name = %s, description = %s, supplier = %s, price = %s WHERE code = %s"
        cursor.execute(sql, (int(product_data['code']), product_data['name'], product_data['description'], product_data['supplier'], product_data['price'], product_id))
    connection.commit()

    return jsonify({'message': 'Product updated successfully!'}), 200

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Delete product from the database
    with connection.cursor() as cursor:
        sql = "DELETE FROM products WHERE code = %s"
        cursor.execute(sql, (int(product_id),))
    connection.commit()

    return jsonify({'message': 'Product deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')