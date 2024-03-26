import csv

def calculate_yoy_increase(input_file_path, output_file_path):
    with open(input_file_path, mode='r', encoding='utf-8') as infile, open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read the header from the input file and prepare the header for the output file
        input_header = next(reader)
        # Assuming the first three columns do not require YoY calculation, we copy them as is
        output_header = input_header[:3] + [f'{year} YoY Increase (%)' for year in input_header[4:]]  # Adjust to skip the first year for YoY calculation
        
        # Write the modified header to the output file
        writer.writerow(output_header)

        for row in reader:
            # Extract the area information and the yearly data
            area_info = row[:3]
            yearly_data = [float(value) if value not in ['', '0', 0] else 0 for value in row[3:]]

            # Calculate YoY increase
            yoy_increases = []  # Initialize the list for YoY increases
            for i in range(1, len(yearly_data)):
                if yearly_data[i-1] == 0:  # Check if the previous year's value is zero
                    yoy_increase = "N/A"  # Assign a special value or message
                else:
                    yoy_increase = ((yearly_data[i] - yearly_data[i-1]) / yearly_data[i-1]) * 100
                    yoy_increase = round(yoy_increase, 2)
                yoy_increases.append(yoy_increase)

            # Write the area info and YoY increases to the output file
            writer.writerow(area_info + yoy_increases)


if __name__ == "__main__":
    input_csv = "./processed_data/bk_median_saleprice_by_year.csv"  # Replace this with the path to your input CSV file
    output_csv = "./processed_data/yoy_bk_saleprice.csv"  # Replace this with the path you want for your output CSV file
    calculate_yoy_increase(input_csv, output_csv)
