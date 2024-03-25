import pandas as pd
import glob
import os

directory_path = 'BK_RES'  # Replace with your directory path
file_pattern = os.path.join(directory_path, '*.csv')

# Initialize empty DataFrames for AVTOT, FULLVAL, and NUM_PROPERTIES
combined_avtot = pd.DataFrame()
combined_fullval = pd.DataFrame()
combined_num_properties = pd.DataFrame()

for file_path in sorted(glob.glob(file_pattern)):
    print(f"Processing file: {file_path}")
    df = pd.read_csv(file_path)
    
    for year in df['YEAR'].unique():
        year_df = df[df['YEAR'] == year]
        
        # Group by POSTCODE for medians and count
        medians_avtot = year_df.groupby('POSTCODE')['AVTOT'].median().reset_index()
        medians_avtot.columns = ['POSTCODE', f'AVTOT_median{year}']
        medians_fullval = year_df.groupby('POSTCODE')['FULLVAL'].median().reset_index()
        medians_fullval.columns = ['POSTCODE', f'FULLVAL_median{year}']
        num_properties = year_df.groupby('POSTCODE').size().reset_index(name=f'NUM_PROPERTIES{year}')
        
        # Merge with the combined DataFrames
        if combined_avtot.empty:
            combined_avtot = medians_avtot
            combined_fullval = medians_fullval
            combined_num_properties = num_properties
        else:
            combined_avtot = pd.merge(combined_avtot, medians_avtot, on='POSTCODE', how='outer')
            combined_fullval = pd.merge(combined_fullval, medians_fullval, on='POSTCODE', how='outer')
            combined_num_properties = pd.merge(combined_num_properties, num_properties, on='POSTCODE', how='outer')

# Saving to CSV files
combined_avtot.to_csv(os.path.join(directory_path, 'combined_avtot_by_year.csv'), index=False)
combined_fullval.to_csv(os.path.join(directory_path, 'combined_fullval_by_year.csv'), index=False)
combined_num_properties.to_csv(os.path.join(directory_path, 'combined_num_properties_by_year.csv'), index=False)

print('CSV files created:')
print('combined_avtot_by_year.csv')
print('combined_fullval_by_year.csv')
print('combined_num_properties_by_year.csv')

