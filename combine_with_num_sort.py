import pandas as pd
import glob
import os

directory_path = 'BK_RES'
file_pattern = os.path.join(directory_path, '*.csv')

# Initialize empty DataFrames for AVTOT, FULLVAL, and NUM_PROPERTIES
combined_avtot = pd.DataFrame()
combined_fullval = pd.DataFrame()
combined_num_properties = pd.DataFrame()

for file_path in glob.glob(file_pattern):
    print(f"Processing file: {file_path}")
    df = pd.read_csv(file_path)
    
    for year in sorted(df['YEAR'].unique()):
        year_df = df[df['YEAR'] == year]
        
        # Group by POSTCODE for medians and count
        medians_avtot = year_df.groupby('POSTCODE')['AVTOT'].median().reset_index()
        medians_fullval = year_df.groupby('POSTCODE')['FULLVAL'].median().reset_index()
        num_properties = year_df.groupby('POSTCODE').size().reset_index(name=f'NUM_PROPERTIES{year}')
        
        # Rename columns to include the year
        medians_avtot.columns = ['POSTCODE', f'AVTOT_median{year}']
        medians_fullval.columns = ['POSTCODE', f'FULLVAL_median{year}']
        
        # Merge with the combined DataFrames
        combined_avtot = pd.merge(combined_avtot, medians_avtot, on='POSTCODE', how='outer')
        combined_fullval = pd.merge(combined_fullval, medians_fullval, on='POSTCODE', how='outer')
        combined_num_properties = pd.merge(combined_num_properties, num_properties, on='POSTCODE', how='outer')

# Function to sort columns based on years and keep POSTCODE as the first column
def sort_columns_by_year(df):
    year_cols = [col for col in df if col.startswith('NUM_PROPERTIES') or col.startswith('AVTOT_median') or col.startswith('FULLVAL_median')]
    sorted_cols = ['POSTCODE'] + sorted(year_cols, key=lambda x: int(x[-4:]))
    return df[sorted_cols]

# Apply the sorting function to each DataFrame
combined_avtot = sort_columns_by_year(combined_avtot)
combined_fullval = sort_columns_by_year(combined_fullval)
combined_num_properties = sort_columns_by_year(combined_num_properties)

# Save the sorted DataFrames to CSV files
combined_avtot.to_csv(os.path.join(directory_path, 'combined_avtot_by_year_sorted.csv'), index=False)
combined_fullval.to_csv(os.path.join(directory_path, 'combined_fullval_by_year_sorted.csv'), index=False)
combined_num_properties.to_csv(os.path.join(directory_path, 'combined_num_properties_by_year_sorted.csv'), index=False)

print('Sorted CSV files created:')
print('combined_avtot_by_year_sorted.csv')
print('combined_fullval_by_year_sorted.csv')
print('combined_num_properties_by_year_sorted.csv')

