# ===================================================
# File: metadata_csv_reader.py
# Author: Trent Bultsma
# Date: 3/28/2023
# Description: Reads metadata from a csv file.
# ==================================================

import csv

def read_metadata_csv(metadata_csv_file_name:str) -> dict:
    """Reads and returns the metadata from the inputted csv file.
    
    Args:
        metadata_csv_file_name (str): the name of the csv file containing metadata.
    """
    # files are formatted with many rows of a certain group id which can be collapsed into one row
    collapsed_rows = {}

    with open(metadata_csv_file_name, "r", newline="") as metadata_file:
        csv_reader = csv.DictReader(metadata_file)

        # collapse them into one row
        for row in csv_reader:
            # add the row's group id to the collapsed rows if it isn't there
            if row["GROUP_ID"] not in collapsed_rows.keys():
                collapsed_rows[row["GROUP_ID"]] = dict()
            
            collapsed_row = collapsed_rows[row["GROUP_ID"]]
            # update the collapsed row with everything from this row
            # (skip the left 2 columns because they are row labels that don't need collapsing)
            for field, value in list(row.items())[2:]:
                # make sure we don't overwrite anything in the collapsing process
                # (theoretically this should never happen, but if it does that would be an issue)
                if field in collapsed_row.keys() and collapsed_row[field] != "":
                    # the existing value is being overwritten by something else (not good)
                    if value != "":
                        raise Exception("Error in collapsing a row. Trying to overwrite value " + str(collapsed_row[field]) + " with value " + str(value))
                else:
                    collapsed_row[field] = value
    
    # map the metadata to the file name instead of group id
    file_name_metadata = dict()
    for row in collapsed_rows.values():
        file_name_metadata[row["FILE_FILEURL"]] = row

    return file_name_metadata