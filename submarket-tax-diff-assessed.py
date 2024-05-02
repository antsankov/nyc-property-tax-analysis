import pandas as pd
import json

# Load the sales price data
sales_data = pd.read_csv('./processed_data/bk_CLEANED_median_saleprice_by_year.csv')

# Load the AVTOT data with simplified year columns
avtot_data = pd.read_csv('./processed_data/cleaned_combined_avtot_by_year.csv')

# Load the neighborhood data
with open('neighborhoods.json', 'r') as file:
    neighborhoods = json.load(file)

# Organize data by submarkets, aggregating zip codes under each submarket
submarkets = {}
for neighborhood, details in neighborhoods.items():
    submarket = details['submarket']
    if submarket not in submarkets:
        submarkets[submarket] = set()
    submarkets[submarket].update(details['zip'])

# Map sales data years to AVTOT years
year_map = {str(y): str(y) for y in range(2011, 2020)}

# Create a new DataFrame to store the differences
results = pd.DataFrame(columns=['Submarket'] + list(year_map.keys()))

# Process each submarket
for submarket, zip_codes in submarkets.items():
    # Filter AVTOT data for current submarket zip codes
    submarket_avtot = avtot_data[avtot_data['POSTCODE'].isin(zip_codes)]

    if submarket_avtot.empty:
        print(f"No AVTOT data found for Submarket {submarket} with ZIPs {zip_codes}")
        continue

    # Calculate average AVTOT for the submarket across its ZIP codes
    avg_avtot = submarket_avtot.mean()

    # Calculate the difference per year and prepare a row to append to results
    differences = {'Submarket': submarket}
    for year, mapped_year in year_map.items():
        sales_col = str(year)
        avtot_col = str(mapped_year)
        # Aggregate sales data for the submarket
        submarket_sales = sales_data[sales_data['ZipCode'].isin(zip_codes)]
        if not submarket_sales.empty:
            avg_sales = submarket_sales[sales_col].mean() if sales_col in submarket_sales.columns else 0
            differences[year] = int(avg_sales - avg_avtot[avtot_col]) if avtot_col in avg_avtot else None

    results = results._append(differences, ignore_index=True)

# Calculate overall averages for all Brooklyn
all_brooklyn_zips = {zip for zips in submarkets.values() for zip in zips}
all_brooklyn_avtot = avtot_data[avtot_data['POSTCODE'].isin(all_brooklyn_zips)].mean()
brooklyn_differences = {'Submarket': 'Brooklyn'}
for year, mapped_year in year_map.items():
    sales_col = str(year)
    avtot_col = str(mapped_year)
    # Aggregate sales data for all Brooklyn
    brooklyn_sales = sales_data[sales_data['ZipCode'].isin(all_brooklyn_zips)]
    if not brooklyn_sales.empty:
        avg_sales = brooklyn_sales[sales_col].mean() if sales_col in brooklyn_sales.columns else 0
        brooklyn_differences[year] = int(avg_sales - all_brooklyn_avtot[avtot_col]) if avtot_col in all_brooklyn_avtot else None

results = results._append(brooklyn_differences, ignore_index=True)

# Save results to a new CSV file
results.to_csv('submarket_assessed_price_tax_difference_with_brooklyn.csv', index=False)
