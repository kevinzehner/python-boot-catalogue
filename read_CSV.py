import pandas as pd
import sqlite3

# This script reads a CSV file and writes its contents to an SQLite database.
# - The CSV file path is specified.
# - The CSV file is read into a pandas DataFrame.
# - The DataFrame is written to an SQLite database named 'boots.db' with a table named 'boots'.
# - If the table already exists, it is replaced.

def csv_to_sqlite(csv_file_path, db_file_path):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        conn = sqlite3.connect(db_file_path)

        # Write the DataFrame to the SQLite database
        # Table name will be 'boots'
        df.to_sql("boots", conn, if_exists="replace", index=False)
        print("Data successfully written to the database.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
      
        if "conn" in locals():
            conn.close()

csv_file_path = "boots.csv"  
db_file_path = "boots.db"  


csv_to_sqlite(csv_file_path, db_file_path)
