import sqlite3


def print_tables_and_columns(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", tables)

    # Get the columns of the boots table
    if ("boots",) in tables:
        cursor.execute("PRAGMA table_info(boots);")
        columns = cursor.fetchall()
        print("Columns in 'boots' table:")
        for column in columns:
            print(column)
    else:
        print("Table 'boots' does not exist in the database.")

    conn.close()


db_path = "boots.db"  # Adjust the path as needed
print_tables_and_columns(db_path)
