import json, sys
import requests
import pandas as pd

def check_joblists(company_id):
    url = f'https://www.104.com.tw/company/ajax/joblist/options/{company_id}'
    headers = {
        'Host': 'www.104.com.tw',
        'Referer': f'https://www.104.com.tw/company/{company_id}',

        # mimic the headers, payload, user-agent, etc.
        # https://stackoverflow.com/questions/42237672/python-toomanyredirects-exceeded-30-redirects
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }
    main_r = requests.get(url, headers=headers)
    return main_r.json()['data']['jobCount'] != 0

def search(searched_word='power platform', company='Realtek'):
    """
    :param searched_word: the keyword str you want to search in lower case
    :param company: the target company
    """
    print(f'searched_word="{searched_word}", company="{company}"')
    with open('company-match.json', 'r') as my_json:
        company_dict = json.load(my_json)
    company_id = company_dict[company]

    potential_jobs = []

    if not check_joblists(company_id):
        print(f'There is no jobs opening in {company}')
        return potential_jobs

    url = f'https://www.104.com.tw/company/ajax/joblist/{company_id}'
    headers = {
        'Host': 'www.104.com.tw',
        'Referer': f'https://www.104.com.tw/company/{company_id}'
    }
    main_r = requests.get(url, headers=headers)
    pages = main_r.json()['data']['totalPages']

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
    print(f'{company} result len={len(potential_jobs)}')
    return potential_jobs

if __name__ == '__main__':
    search(
        searched_word=sys.argv[2],
        company=sys.argv[1]
    )