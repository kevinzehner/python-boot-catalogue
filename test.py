import pandas as pd
import sqlite3

try:
    # Path to your CSV file
    csv_file_path = "boots.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Connect to the SQLite database
    conn = sqlite3.connect("boots.db")

    # Write the DataFrame to the SQLite database
    # Table name will be 'boots'
    df.to_sql("boots", conn, if_exists="replace", index=False)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the database connection
    if "conn" in locals():
        conn.close()
