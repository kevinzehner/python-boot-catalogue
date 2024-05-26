import pandas as pd
import sqlite3


def update_column_name(conn):
    cursor = conn.cursor()

    # Drop the new table if it already exists
    cursor.execute("DROP TABLE IF EXISTS wheelbearing_LSODS_new")

    # Step 1: Create a new table with the updated schema
    cursor.execute(
        """
    CREATE TABLE wheelbearing_LSODS_new (
        Manuf TEXT,
        Model TEXT,
        EngineSize TEXT,
        mark_series TEXT,
        TRWDansDRWDive TEXT,
        MPos TEXT,
        LSODS_PartNumber TEXT,
        Bearing_1_Size TEXT,
        jpeg TEXT
    )
    """
    )

    # Step 2: Copy data from the old table to the new table
    cursor.execute(
        """
    INSERT INTO wheelbearing_LSODS_new (Manuf, Model, EngineSize, mark_series, TRWDansDRWDive, MPos, LSODS_PartNumber, Bearing_1_Size, jpeg)
    SELECT Manuf, Model, EngineSize, mark_series, TRWDansDRWDive, MPos, [LSODS PartNumber] AS LSODS_PartNumber, Bearing_1_Size, jpeg
    FROM wheelbearing_LSODS
    """
    )

    # Step 3: Drop the old table
    cursor.execute("DROP TABLE wheelbearing_LSODS")

    # Step 4: Rename the new table to the old table name
    cursor.execute("ALTER TABLE wheelbearing_LSODS_new RENAME TO wheelbearing_LSODS")

    conn.commit()


try:
    csv_file_path = "wheelbearing_rows.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Connect to the SQLite database
    conn = sqlite3.connect("wheelbearings_LSODS.db")

    # Write the DataFrame to the SQLite database
    df.to_sql("wheelbearing_LSODS", conn, if_exists="replace", index=False)

    # Update the column names in the SQLite database
    update_column_name(conn)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()
