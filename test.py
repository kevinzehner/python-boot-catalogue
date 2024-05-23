import pandas as pd
import sqlite3

try:
  
    csv_file_path = "wheelbearing_rows.csv"

    df = pd.read_csv(csv_file_path)

    conn = sqlite3.connect("wheelbearings_LSODS.db")

    df.to_sql("wheelbearing_LSODS", conn, if_exists="replace", index=False)

except Exception as e:
    print(f"An error occurred: {e}")

finally:

    conn.close()
