import csv


class VariableNames:
    country_code_origin = 'COUNTRY'
    country_code = 'country_code'
    year_origin = 'Time'
    year = 'year'
    month = 'month'
    hours_worked_origin = 'Value'
    hours_worked = 'Hours worked per year'
    employment_status = 'EMPSTAT'



new_data = []

with open('data/Employment data.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    print(reader.fieldnames)
    for row in reader:
        if int(row[VariableNames.year_origin]) >= 2000 and row[VariableNames.employment_status] == 'DE':
            hours_worked = 'N/A'
            if row[VariableNames.hours_worked_origin]:
                hours_worked = row[VariableNames.hours_worked_origin]
            for i in range(1, 13):
                new_data.append({VariableNames.country_code: row[VariableNames.country_code_origin],
                                 VariableNames.year: row[VariableNames.year_origin],
                                 VariableNames.month: i,
                                 VariableNames.hours_worked: hours_worked})
print(new_data)

out_file_name = 'data/processed/hours_worked.csv'
with open(out_file_name, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[VariableNames.country_code,
                                           VariableNames.year,
                                           VariableNames.month,
                                           VariableNames.hours_worked])
    writer.writeheader()
    writer.writerows(new_data)
