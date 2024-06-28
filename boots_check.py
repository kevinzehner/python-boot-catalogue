import sqlite3
import re


def find_mismatched_part_numbers(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch PartNumber and ModInd columns
    cursor.execute("SELECT PartNumber, ModInd FROM boots")
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Prepare to collect mismatches
    mismatched_part_numbers = set()
    none_part_numbers = set()  # Set to track unique PartNumbers with None in ModInd

    for part_number, mod_ind in data:
        # Track unique PartNumbers with None in ModInd
        if mod_ind is None:
            none_part_numbers.add(part_number)
            continue

        # Extract the numeric part from PartNumber and ModInd
        part_number_num = re.sub(r"^KL", "", part_number)
        mod_ind_num = re.sub(r"^JB|\.jpg$", "", mod_ind)

        # Compare the numeric parts
        if part_number_num != mod_ind_num:
            mismatched_part_numbers.add(part_number)

    # Include the unique None PartNumbers in mismatches
    mismatched_part_numbers.update(none_part_numbers)

    # Count the number of unique mismatched PartNumbers
    unique_mismatch_count = len(mismatched_part_numbers)
    unique_none_count = len(none_part_numbers)

    return mismatched_part_numbers, unique_mismatch_count, unique_none_count


# Usage
db_path = "boots.db"  # Update this to the path of your database
mismatched_part_numbers, unique_mismatch_count, unique_none_count = (
    find_mismatched_part_numbers(db_path)
)

print(f"Unique mismatched PartNumbers: {mismatched_part_numbers}")
print(f"Count of unique mismatches: {unique_mismatch_count}")
print(f"Count of unique None values in ModInd: {unique_none_count}")
