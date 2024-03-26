import csv

# Input and output file names
input_csv_file = 'processed_data/cleaned_combined_fullval_by_year.csv'
output_csv_file = 'processed_data/yoy_fullval_percentage_increase.csv'

def calculate_year_over_year_increase(row):
    """
    Calculate and return the year-over-year percentage increases for a given row,
    each rounded to two decimal places. Assumes empty cells are zero.
    """
    percentages = []
    for i in range(1, len(row)-1):
        previous_year_value = float(row[i]) if row[i] else 0
        current_year_value = float(row[i+1]) if row[i+1] else 0
        if previous_year_value == 0:
            year_over_year_percentage = 0
        else:
            year_over_year_percentage = round(((current_year_value - previous_year_value) / previous_year_value) * 100, 2)
        percentages.append(year_over_year_percentage)
    return percentages

with open(input_csv_file, newline='') as csvfile, open(output_csv_file, 'w', newline='') as outputfile:
    csvreader = csv.reader(csvfile)
    csvwriter = csv.writer(outputfile)
    
    # Skip header row in the input file and prepare a header for the output file
    headers = next(csvreader)
    new_headers = headers[0:1] + [f"YOY_{header}" for header in headers[1:-1]]  # Adjust headers for output
    csvwriter.writerow(new_headers)
    
    for row in csvreader:
        year_over_year_percentages = calculate_year_over_year_increase(row)
        output_row = [row[0]] + year_over_year_percentages  # Combine POSTCODE with calculated percentages
        csvwriter.writerow(output_row)

print(f"Year-over-year percentage increases have been written to {output_csv_file}.")
