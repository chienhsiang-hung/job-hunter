import requests
import pandas as pd

header = {
    'Host': 'www.104.com.tw',
    'Referer': 'https://www.104.com.tw/company/salary/all/',

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
url = 'https://www.104.com.tw/company/ajax/salary/list'
main_r = requests.get(url, headers=header).json()['data']
pd.DataFrame.from_records(main_r).sort_values('medianNonSupervisor', ascending=False).to_csv('salary_list.csv')