import json
import pandas as pd
from search import Search

with open('company-match.json', 'r') as my_json:
    company_dict = json.load(my_json)

search = Search()
potential_jobs = []
for company in company_dict:
    result = search.search(searched_word='power automate', company=company)
    if len(result) > 0: potential_jobs += result

df = pd.DataFrame.from_records(potential_jobs)
df.to_excel(f'Result.xlsx')

print(f'Total len={len(potential_jobs)}')
print(df)