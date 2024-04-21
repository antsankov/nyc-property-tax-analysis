import pandas as pd
import json

# Load the sales price data
sales_data = pd.read_csv('./processed_data/bk_CLEANED_median_saleprice_by_year.csv')

# Load the AVTOT data with simplified year columns
avtot_data = pd.read_csv('./processed_data/cleaned_combined_avtot_by_year.csv')

# Load the neighborhood data
with open('neighborhoods.json', 'r') as file:
    neighborhoods = json.load(file)

# Map sales data years to AVTOT years (now directly use year since AVTOT data columns are just years)
year_map = {
    '2011': '2011',
    '2012': '2012',
    '2013': '2013',
    '2014': '2014',
    '2015': '2015',
    '2016': '2016',
    '2017': '2017',
    '2018': '2018',
    '2019': '2019'
}

# Create a new DataFrame to store the differences
results = pd.DataFrame(columns=['Neighborhood+ZIP'] + list(year_map.keys()))

# Process each neighborhood in the sales data
for index, row in sales_data.iterrows():
    neighborhood = row['areaName']
    if neighborhood not in neighborhoods:
        continue  # skip if neighborhood isn't in the lookup

    zip_codes = neighborhoods[neighborhood]['zip']
    neighborhood_avtot = avtot_data[avtot_data['POSTCODE'].isin(zip_codes)]

    if neighborhood_avtot.empty:
        print(f"No AVTOT data found for {neighborhood} with ZIPs {zip_codes}")
        continue

    # Calculate average AVTOT for the neighborhood across its ZIP codes
    avg_avtot = neighborhood_avtot.mean()

    # Prepare the neighborhood name with ZIP codes
    neighborhood_zip = f"{neighborhood} ({';'.join(map(str, zip_codes))})"

    # Calculate the difference per year and prepare a row to append to results
    differences = {'Neighborhood+ZIP': neighborhood_zip}
    for year, mapped_year in year_map.items():
        sales_col = str(year)
        avtot_col = str(mapped_year)
        if sales_col in row and avtot_col in avg_avtot:
            differences[year] = row[sales_col] - avg_avtot[avtot_col]

    results = results._append(differences, ignore_index=True)

# Save results to a new CSV file
results.to_csv('neighborhood_assesed_price_tax_difference.csv', index=False)
