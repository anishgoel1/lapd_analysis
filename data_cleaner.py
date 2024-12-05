"""
LAPD Crime Data Cleaner

This script processes the LAPD crime dataset by removing unnecessary columns
and cleaning up formatting.

Input file: crime_data_lapd.csv
"""

import pandas as pd

# Read the crime data
df = pd.read_csv("crime_data_lapd.csv")

# Remove non-essential columns
df = df.drop(
    columns=[
        "DR_NO",  # Division of Records Number
        "Date Rptd",  # Date Reported
        "AREA",  # LAPD Area ID
        "Rpt Dist No",  # Report District Number
        "Part 1-2",  # Crime Category
        "Crm Cd",  # Crime Code
        "Mocodes",  # Modus Operandi Codes
        "Premis Cd",  # Premise Code
        "Weapon Used Cd",  # Weapon Code
        "Status",  # Status Code
        "Status Desc",  # Status Description
        "Crm Cd 1",  # Additional Crime Code 1
        "Crm Cd 2",  # Additional Crime Code 2
        "Crm Cd 3",  # Additional Crime Code 3
        "Crm Cd 4",  # Additional Crime Code 4
    ]
)

# Clean up the date format by removing the time component
df["DATE OCC"] = df["DATE OCC"].str.replace(" 12:00:00 AM", "", regex=False)

# Create a mapping dictionary for victim descent codes
descent_mapping = {
    "A": "Other Asian",
    "B": "Black",
    "C": "Chinese",
    "D": "Cambodian",
    "F": "Filipino",
    "G": "Guamanian",
    "H": "Hispanic/Latin/Mexican",
    "I": "American Indian/Alaskan Native",
    "J": "Japanese",
    "K": "Korean",
    "L": "Laotian",
    "O": "Other",
    "P": "Pacific Islander",
    "S": "Samoan",
    "U": "Hawaiian",
    "V": "Vietnamese",
    "W": "White",
    "X": "Unknown",
    "Z": "Asian Indian",
}

# Replace the single letters with full descriptions
df["Vict Descent"] = df["Vict Descent"].replace(descent_mapping)

# Create a mapping dictionary for victim sex codes
sex_mapping = {"F": "Female", "M": "Male", "X": "Unknown"}

# Replace the single letters with full descriptions
df["Vict Sex"] = df["Vict Sex"].replace(sex_mapping)

# Display first 5 rows
print(df.head())

# Save the cleaned DataFrame as a pickle file
df.to_pickle("cleaned_crime_data.pkl")
