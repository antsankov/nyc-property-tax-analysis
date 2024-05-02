import csv
import json

def load_data(csv_filename, json_filename):
    # Load CSV data
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_data = {int(row['POSTCODE']): {year: float(row[year]) for year in reader.fieldnames if year != 'POSTCODE'} for row in reader}

    # Load JSON data
    with open(json_filename) as jsonfile:
        json_data = json.load(jsonfile)

    return csv_data, json_data

def aggregate_by_submarket(csv_data, json_data):
    # Create a dictionary to store sums and counts for averaging
    submarket_data = {}
    # Map from zip to submarket
    zip_to_submarket = {}
    for neighborhood, info in json_data.items():
        submarket = info['submarket']
        for zip_code in info['zip']:
            zip_to_submarket[zip_code] = submarket
            if submarket not in submarket_data:
                submarket_data[submarket] = {}

    # Aggregate data by submarket
    for zip_code, yearly_data in csv_data.items():
        submarket = zip_to_submarket.get(zip_code)
        if submarket:
            for year, value in yearly_data.items():
                if year not in submarket_data[submarket]:
                    submarket_data[submarket][year] = {'sum': 0, 'count': 0}
                submarket_data[submarket][year]['sum'] += value
                submarket_data[submarket][year]['count'] += 1

    # Calculate averages
    averages_by_submarket = {}
    for submarket, yearly_data in submarket_data.items():
        averages_by_submarket[submarket] = {}
        for year, data in yearly_data.items():
            average = data['sum'] / data['count']
            averages_by_submarket[submarket][year] = int(average)

    return averages_by_submarket

def write_to_csv(averages_by_submarket, output_filename):
    with open(output_filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        # Write header
        headers = ['Submarket'] + sorted(next(iter(averages_by_submarket.values())).keys())
        csv_writer.writerow(headers)
        
        # Write data rows
        for submarket, yearly_averages in sorted(averages_by_submarket.items()):
            row = [submarket] + [yearly_averages[year] for year in sorted(yearly_averages)]
            csv_writer.writerow(row)

def main():
    csv_filename = './processed_data/cleaned_combined_avtot_by_year.csv'
    json_filename = 'neighborhoods.json'
    output_filename = 'averages_by_submarket.csv'

    csv_data, json_data = load_data(csv_filename, json_filename)
    averages_by_submarket = aggregate_by_submarket(csv_data, json_data)
    write_to_csv(averages_by_submarket, output_filename)
    print("Data has been written to", output_filename)

if __name__ == "__main__":
    main()
