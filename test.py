import pandas as pd
import sqlite3

try:
  
    csv_file_path = "data.csv"

    df = pd.read_csv(csv_file_path)

    conn = sqlite3.connect("wheelbearings.db")

    df.to_sql("wheelbearing", conn, if_exists="replace", index=False)

except Exception as e:
    print(f"An error occurred: {e}")

finally:

    conn.close()
