import pandas as pd

# Load the cleaned DataFrame
df = pd.read_pickle('cleaned_crime_data.pkl')

# Print the first 5 rows of the DataFrame
print(df.head())
