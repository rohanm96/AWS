import pymysql
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Database connection
connection = pymysql.connect(
    host='devopsdemodb.cdtqd6jgia7i.ap-south-1.rds.amazonaws.com',
    user='admin',
    password='admin123',
    db='testdb',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


# Database connection info
db_host = 'devopsdemodb.cdtqd6jgia7i.ap-south-1.rds.amazonaws.com'
db_user = 'admin'
db_password = 'admin123'
db_name = 'testdb'
charset='utf8mb4'
cursorclass=pymysql.cursors.DictCursor



# Connect to the database
def get_db_connection():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, cursorclass=pymysql.cursors.DictCursor)

# Home route displays all products
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productsnew;')
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', products=products)

# Route to add a new product
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productsnew (name, price, description) VALUES (%s, %s, %s);', (name, int(price), description))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

# Route to update a product
@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        
        cursor.execute('UPDATE productsnew SET name = %s, price = %s, description = %s WHERE id = %s;', (name, price, description, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM productsnew WHERE id = %s;', (id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('update.html', product=product)

# Route to delete a product
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productsnew WHERE id = %s;', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)