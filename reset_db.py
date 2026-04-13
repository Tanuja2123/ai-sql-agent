import duckdb
import sqlite3
import pandas as pd

# Delete old SQLite and rebuild it cleanly
duck = duckdb.connect('ecommerce.db')
con = sqlite3.connect('ecommerce_sqlite.db')

for table in ['products', 'customers', 'orders']:
    df = duck.execute(f'SELECT * FROM {table}').df()
    df.to_sql(table, con, if_exists='replace', index=False)
    print(f"Restored {table}: {len(df)} rows")

duck.close()
con.close()
print("Done! Database restored.")