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
    # files are formatted with many rows of a certain group id which can
    #  be collapsed into one row with a list of elements for each field
    collapsed_rows = {}

    with open(metadata_csv_file_name, "r", newline="") as metadata_file:
        csv_reader = csv.DictReader(metadata_file)

        # collapse them into one row
        for row in csv_reader:
            # add the row's group id to the collapsed rows if it isn't there
            if row["GROUP_ID"] not in collapsed_rows.keys():
                collapsed_rows[row["GROUP_ID"]] = dict()
            
            # set the specific collapsed row to be the newly initialized dictionary
            # we just made, which is stored in the overall rows datastructure
            collapsed_row = collapsed_rows[row["GROUP_ID"]]
            # update the collapsed row with everything from this row
            # (skip the left 2 columns because they are row labels that don't need collapsing)
            for field, value in list(row.items())[2:]:
                # initialize the list for the field if it pops up for the first time
                if field not in collapsed_row.keys():
                    collapsed_row[field] = []
                # add the value to the list as long as it is not an empty element
                if value != "":
                    collapsed_row[field].append(value)
    
    # map the metadata to the file name instead of group id
    file_name_metadata = dict()
    for row in collapsed_rows.values():
        # we can use index 0 in this case becase there will only ever be one file url
        file_name_metadata[row["FILE_FILEURL"][0]] = row

    return file_name_metadata