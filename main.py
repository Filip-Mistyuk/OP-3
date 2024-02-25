import sqlite3

db = sqlite3.connect("shop.db")

# db.execute('''CREATE TABLE products (
#     product_id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL,
#     category TEXT NOT NULL,
#     price REAL NOT NULL
# );''')

# db.execute('''CREATE TABLE customers ( customer_id INTEGER PRIMARY KEY,
#             first_name TEXT NOT NULL,
#             last_name TEXT NOT NULL,
#             email TEXT NOT NULL UNIQUE );''')

# db.execute('''CREATE TABLE orders ( order_id INTEGER PRIMARY KEY,
#             customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
#             quantity INTEGER NOT NULL, order_date DATE NOT NULL,
#             FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
#             FOREIGN KEY (product_id) REFERENCES products(product_id) );''')


def add_product(db, name: str, category: str, price: int):
        db.execute("INSERT INTO products (name, category, price) VALUE(?, ?, ?)", (name, category, price))
        db.commit()

def add_customer(db, first_name:str, last_name:str, email:str):
    db.execute(''' INSERT into customers(first_name, last_name, email) VALUES(?,?,?)''',(first_name, last_name, email))
    db.commit()  

def Make_order(db, customer_id, product_id, quantity):
    db.execute(''' INSERT into orders(customer_id, product_id, quantity, order_date)
                VALUES(?,?,?, CURRENT_TIMESTAMP) ''',(customer_id, product_id, quantity))
    db.commit() 

def get_total_income(db):
    query = db.execute('''SELECT SUM(products.price * orders.quantity) AS total_bill
        FROM orders
        INNER JOIN products ON orders.order_id = products.product_id''')
    return query.fetchone()

def order_quantity(db):
    query = db.execute('''SELECT customers.first_name AS customer_name,
                       COUNT(orders.order_id) AS amount_of_orders
                       FROM orders
                       INNER JOIN customer ON orders.customer_id = customers.customer_id
                       GROUP BY customers.first_name
                       ORDER BY customers.customer_id ASC''')
    return query.fetchall()

def avg_bill(db):
    r = db.execute('''SELECT AVG(products.price * orders.quantity) AS avg_bill
                   FROM orders
                   INNER JOIN products ON orders.order_id = products.product_id
                   ''')
    return r.fetchone()

def the_most_popular_product_category(db):
    r = db.execute('''SELECT products.category, SUM(orders.quantity) AS total_order_quantity
                   FROM orders
                   INNER JOIN products ON orders.product_id = products.product_id
                   GROUP BY products.category
                   ORDER BY total_order_quantity DESC''')
    return r.fetchone()[0]

def increase_value_of_phones_by_10_percents(db):
    db.execute('''UPDATE products
                SET price = price * 1.1
                WHERE category = "Phones"''')
    
def show_all_customers(db):
    r = db.execute('''SELECT first_name, last_name FROM customers''')
    return r.fetchall()

def show_all_products(db):
    r = db.execute('''SELECT name FROM products''')
    return r.fetchall()

def show_all_orders(db):
    r = db.execute('''SELECT * FROM orders''')
    return r.fetchall()

while True:
    print('''
Що ви хочете зробити?

1 - Додавання продуктів:
2 - Додавання клієнтів:
3 - Замовлення товарів:
4 - Сумарний обсяг продажів:
5 - Кількість замовлень на кожного клієнта:
6 - Середній чек замовлення:
7 - Найбільш популярна категорія товарів:
8 - Загальна кількість товарів кожної категорії:
9 - Оновлення цін категорії на 10% більші:
10 - Показати усіх користувачів
11 - Показати усі продукти
12 - Показати усі замовлення(Joined)
0 - Вийти:

        ''')
    command = int(input("Обирайте: "))
    if command == 1:
        name = input("name: ")
        category = input("category: ")
        price = input("price: ")
        add_product(db, name, category, price)
        print(f"product {name} added...")

    if command == 2:
        first_name = input('first name: ')
        last_name = input('last name: ')
        email = input('email: ')
        add_customer(db, first_name, last_name, email)
        print(f'customer {first_name} {last_name} added')

    if command == 3:
        customer_id = int(input("id customer: "))
        product_id = int(input("id product: "))
        quantity = int(input("quantity: "))
        Make_order(db, customer_id, product_id, quantity)

    if command == 4:
        print(get_total_income(db))

    if command == 5:
        print(order_quantity(db))
        
    if command == 6:
        print(avg_bill(db))

    if command == 7:
        print(the_most_popular_product_category(db))

    if command == 8:
        increase_value_of_phones_by_10_percents(db)

    if command == 9:
        print(show_all_customers(db))

    if command == 10:
        print(show_all_products(db))

    if command == 11:
        print(show_all_orders(db))
        