import requests
import pandas as pd
import json

with open('company-match.json', 'r') as my_json:
    company_dict = json.load(my_json)
searched_word = 'power'
company = company_dict['Realtek']

url = f'https://www.104.com.tw/company/ajax/joblist/{company}'
headers = {
    'Host': 'www.104.com.tw',
    'Referer': f'https://www.104.com.tw/company/{company}'
}
main_r = requests.get(url, headers=headers)

pages = main_r.json()['data']['totalPages']

potential_jobs = []
# outer loop for pages
for p in range(1, int(pages)+1):
    sub_r = requests.get(url+f'?page={p}', headers=headers)
    sub_r_json = sub_r.json()['data']['list']

    # inner loop for jobs
    if 'topJobs' in sub_r_json:
        for job in sub_r_json['topJobs']:
            if searched_word in job['jobDescription'].lower():
                potential_jobs.append(job)
    for job in sub_r_json['normalJobs']:
        if searched_word in job['jobDescription'].lower():
            potential_jobs.append(job)

pd.DataFrame.from_records(potential_jobs).to_excel(f'Result.xlsx')
print(len(potential_jobs), potential_jobs)