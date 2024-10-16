import json
import pandas as pd
from search import Search

with open('company-match.json', 'r') as my_json:
    company_dict = json.load(my_json)

search = Search()
potential_jobs = []
for i, company in enumerate(company_dict):
    # enumerate for testing purpose
    # if i==2: break
    result = search.search(searched_word='power automate', company=company)
    if len(result) > 0: potential_jobs += result

df = pd.DataFrame.from_records(potential_jobs)
df.to_excel(f'Result.xlsx')
with open('Result.json', 'w') as f:
    json.dump(potential_jobs, f, indent=4)

print(f'Total len={len(potential_jobs)}')
print(df)