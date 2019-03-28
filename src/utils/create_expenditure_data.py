import csv


class VariableNames:
    country_code = 'country_code'
    year = 'year'
    month = 'month'
    domestic_gov_expenditure = 'Domestic general government health expenditure per capita, PPP (current international $)'
    domestic_private_expenditure = 'Domestic private health expenditure per capita, PPP (current international $)'
    domestic_total_expenditure = 'Domestic total healthcare expenditure per capita per month, PPP (current international $)'


new_data = []

with open('data/health_indicators.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if int(row[VariableNames.year]) >= 2000:
            total_domestic_spending = 'N/A'
            if row[VariableNames.domestic_gov_expenditure] and row[VariableNames.domestic_private_expenditure]:
                total_domestic_spending = str((float(row[VariableNames.domestic_gov_expenditure])
                                              + float(row[VariableNames.domestic_private_expenditure])) / 12.)
            for i in range(1, 13):
                new_data.append({VariableNames.country_code: row[VariableNames.country_code],
                                 VariableNames.year: row[VariableNames.year],
                                 VariableNames.month: i,
                                 VariableNames.domestic_total_expenditure: total_domestic_spending})
# print(new_data)

out_file_name = 'data/processed/domestic_healthcare_spending.csv'
with open(out_file_name, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[VariableNames.country_code,
                                           VariableNames.year,
                                           VariableNames.month,
                                           VariableNames.domestic_total_expenditure])
    writer.writeheader()
    writer.writerows(new_data)
