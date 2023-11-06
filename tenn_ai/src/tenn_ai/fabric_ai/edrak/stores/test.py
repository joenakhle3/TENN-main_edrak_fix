import os
from tenn_ai.fabric_ai.edrak.stores.tenn_sql_db import TENN_SqlDB
from pandas import DataFrame

result: DataFrame = None

# Create a new database
db = TENN_SqlDB(passed_verbose=True)
engine = db.connect()

# Create a new table
query = "CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name VARCHAR(50), coolness INTEGER);"
result = db.query(query)

# Retrieve the row
query = "SELECT * FROM test_table WHERE coolness > 66;"
result = db.query(query)

# Insert a new row
query = "INSERT INTO test_table (name, coolness) VALUES ('Firas', 78);"
result = db.query(query)

# Insert a new row
query = "INSERT INTO test_table (name, coolness) VALUES ('Charbel', 88);"
result = db.query(query)

# Insert a new row
query = "INSERT INTO test_table (name, coolness) VALUES ('Joe', 99);"
result = db.query(query)

# Retrieve the row
query = "SELECT * FROM test_table;"
result = db.query(query)

# Retrieve the row
query = "SELECT * FROM test_table WHERE name = 'Joe';"
result = db.query(query)

# Delete the row
query = "DELETE FROM test_table WHERE name = 'Firas';"
result = db.query(query)

# Delete the table
query = "DROP TABLE IF EXISTS test_table;"
result = db.query(query)

