import duckdb
import random
from datetime import datetime, timedelta

con = duckdb.connect('ecommerce.db')

# ── Create tables ─────────────────────────────────────────

con.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id   INTEGER,
        name         VARCHAR,
        category     VARCHAR,
        price        FLOAT,
        stock        INTEGER
    )
''')

con.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id  INTEGER,
        name         VARCHAR,
        city         VARCHAR,
        signup_date  DATE
    )
''')

con.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id     INTEGER,
        customer_id  INTEGER,
        product_id   INTEGER,
        quantity     INTEGER,
        amount       FLOAT,
        order_date   DATE,
        status       VARCHAR
    )
''')

# ── Seed products ─────────────────────────────────────────

categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
product_names = [
    'Wireless Headphones', 'Running Shoes', 'Python Cookbook',
    'Coffee Maker', 'Yoga Mat', 'Laptop Stand', 'T-Shirt',
    'Novel: The Alchemist', 'Smart Watch', 'Desk Lamp'
]
prices = [2999, 1499, 499, 2199, 799, 1299, 399, 299, 4999, 699]

products = [
    (i+1, product_names[i], categories[i % 5], prices[i], random.randint(5, 200))
    for i in range(10)
]
con.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products)

# ── Seed customers ────────────────────────────────────────

cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune', 'Hyderabad']
first_names = ['Arjun', 'Priya', 'Rohan', 'Sneha', 'Karan',
               'Anita', 'Vikram', 'Meera', 'Suresh', 'Divya']
last_names  = ['Sharma', 'Patel', 'Gupta', 'Singh', 'Kumar',
               'Mehta', 'Joshi', 'Nair', 'Reddy', 'Iyer']

base_date = datetime(2024, 1, 1)

customers = [
    (
        i + 1,
        f"{first_names[i % 10]} {last_names[i % 10]}",
        cities[i % 6],
        (base_date + timedelta(days=random.randint(0, 365))).date()
    )
    for i in range(50)
]
con.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', customers)

# ── Seed orders ───────────────────────────────────────────

statuses = ['delivered', 'delivered', 'delivered', 'shipped', 'cancelled', 'processing']
# delivered appears 3x so it's the most common — more realistic

orders = []
for i in range(500):
    pid      = random.randint(1, 10)
    qty      = random.randint(1, 5)
    price    = products[pid - 1][3]
    orders.append((
        i + 1,
        random.randint(1, 50),
        pid,
        qty,
        round(price * qty, 2),
        (base_date + timedelta(days=random.randint(0, 365))).date(),
        random.choice(statuses)
    ))

con.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)', orders)

# ── Verify ────────────────────────────────────────────────

print("Database created successfully!")
print()
for table in ['products', 'customers', 'orders']:
    count = con.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
    print(f"  {table}: {count} rows")

print()
print("Sample from orders:")
print(con.execute('SELECT * FROM orders LIMIT 3').df().to_string(index=False))

con.close()