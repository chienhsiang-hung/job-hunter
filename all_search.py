import json
import pandas as pd
import search


with open('company-match.json', 'r') as my_json:
    company_dict = json.load(my_json)

potential_jobs = []
for company in company_dict:
    result = search.search(searched_word='power automate', company=company)
    if len(result) > 0: potential_jobs += result

pd.DataFrame.from_records(potential_jobs).to_excel(f'Result.xlsx')
print(f'Total len={len(potential_jobs)}')