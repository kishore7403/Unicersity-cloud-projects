from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

DB_HOST = 'a3-db.c9aslvwcmv3h.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = '12345678'
DB_NAME = 'a3db'

def create_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_products_table():
    connection = create_db_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        name VARCHAR(100),
        price VARCHAR(100),
        availability BOOLEAN
    )
    """

    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

@app.route('/store-products', methods=['POST'])
def store_products():
    data = request.get_json()

    if 'products' not in data or not isinstance(data['products'], list) or len(data['products']) == 0:
        return 'Invalid JSON body', 400

    connection = create_db_connection()
    cursor = connection.cursor()

    for product in data['products']:
        name = product.get('name')
        price = product.get('price')
        availability = product.get('availability')

        cursor.execute("INSERT INTO products (name, price, availability) VALUES (%s, %s, %s)",
                       (name, price, availability))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Success.'}), 200

@app.route('/list-products', methods=['GET'])
def list_products():
    connection = create_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name, price, availability FROM products")
    products = cursor.fetchall()

    connection.close()

    if len(products) == 0:
        return jsonify({'products': []}), 200

    product_list = []

    for product in products:
        name, price, availability = product
        product_list.append({'name': name, 'price': price, 'availability': bool(availability)})

    return jsonify({'products': product_list}), 200

if __name__ == '__main__':
    create_products_table()
    app.run(host='0.0.0.0', port=80)