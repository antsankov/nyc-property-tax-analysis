import pandas as pd

# Load the dataset
df = pd.read_csv('./STREETEASY_DATA/all_streeteasy_raw.csv')

# Filter out rows where Borough is not 'Brooklyn'
df = df[df['Borough'] == 'Brooklyn']

# The columns representing months and years in the format YYYY-MM
date_columns = df.columns[3:]

# Melt the dataframe to work with the dates
df_melted = df.melt(id_vars=['areaName', 'Borough', 'areaType'], value_vars=date_columns, var_name='date', value_name='value')

# Convert the 'date' column to datetime to easily extract the year
df_melted['date'] = pd.to_datetime(df_melted['date'], errors='coerce')

# Extract the year from the 'date' column
df_melted['year'] = df_melted['date'].dt.year

# Drop the 'date' column as it's no longer needed
df_melted.drop(columns='date', inplace=True)

# Group by 'areaName', 'Borough', 'areaType', and 'year', then calculate the mean.
df_yearly_avg = df_melted.groupby(['areaName', 'Borough', 'areaType', 'year'])['value'].mean().reset_index()

# Fill NaN values with 0 before rounding and converting to int
df_yearly_avg['value'] = df_yearly_avg['value'].fillna(0).round().astype(int)

# Pivot table to have years as columns and areaNames as rows.
df_pivoted = df_yearly_avg.pivot_table(index=['areaName', 'Borough', 'areaType'], columns='year', values='value').reset_index()

# Fill NaN values with 0 (since we know these are supposed to be integer counts, making 0 a sensible default)
df_pivoted = df_pivoted.fillna(0)

# Ensure all columns except for 'areaName', 'Borough', 'areaType' are integers
for col in df_pivoted.columns:
    if col not in ['areaName', 'Borough', 'areaType']:
        df_pivoted[col] = df_pivoted[col].astype(int)

# Save the result to a new CSV file
df_pivoted.to_csv('yearly_averages_brooklyn_ints_corrected.csv', index=False)

print('Yearly averages for Brooklyn have been calculated, rounded to integers, and saved to yearly_averages_brooklyn_ints_corrected.csv.')
