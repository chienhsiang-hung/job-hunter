import json, sys
import requests
import pandas as pd


class Search:
    def __init__(self):

        with open('company-match.json', 'r') as my_json:
            self.company_dict = json.load(my_json)

        self.header = {
            'Host': 'www.104.com.tw',
            'Referer': '',

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

    def setReferer(self, company_id):
        self.header['Referer'] = f'https://www.104.com.tw/company/{company_id}'

    def check_joblists(self, company_id):
        url = f'https://www.104.com.tw/company/ajax/joblist/options/{company_id}'
        main_r = requests.get(url, headers=self.header)
        return main_r.json()['data']['jobCount'] != 0

    def __inner_job_search__(self, _list, _word, cpn):
        '''
        inner loop for jobs
        '''
        potential_jobs = []
        for job in _list:
            if _word in job['jobDescription'].lower():
                job['company'] = cpn
                job['jobUrl'] = f'https:{job['jobUrl']}' # prettify the jobUrl
                potential_jobs.append(job)
        return potential_jobs

    def search(self, searched_word='power platform', company='Realtek', company_id=None):
        """
        :param searched_word: the keyword str you want to search in lower case
        :param company: the target company
        """
        print(f'searched_word="{searched_word}", company="{company}"')

        if not company_id: company_id = self.company_dict[company]

        self.setReferer(company_id)

        potential_jobs = []

        if not self.check_joblists(company_id):
            print(f'There is no jobs opening in {company}')
            return potential_jobs

        url = f'https://www.104.com.tw/company/ajax/joblist/{company_id}'
        # to get the range of the joblists
        main_r = requests.get(url, headers=self.header)
        pages = main_r.json()['data']['totalPages']

        # outer loop for pages
        for p in range(1, int(pages)+1):
            sub_r = requests.get(url+f'?page={p}', headers=self.header)
            sub_r_json = sub_r.json()['data']['list']

            # check `topJobs` and `normalJobs`
            if 'topJobs' in sub_r_json:
                potential_jobs += self.__inner_job_search__(sub_r_json['topJobs'], searched_word, company)
            potential_jobs += self.__inner_job_search__(sub_r_json['normalJobs'], searched_word, company)

        # pd.DataFrame.from_records(potential_jobs).to_excel(f'tmp/Result.xlsx')
        print(f'{company} result len={len(potential_jobs)}')
        if len(potential_jobs) > 0: print(potential_jobs)
        return potential_jobs


if __name__ == '__main__':
    do_search = Search()
    do_search.search(
        searched_word=sys.argv[2],
        company=sys.argv[1]
    )