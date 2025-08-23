from googleapiclient.discovery import build
import pprint
import json

my_api_key = "AIzaSyA9feuXF6nAeh9fuTBT__gksb6doex_F88"
my_cse_id = "165a400ce7fe34dc1"

class GoogleSearchService:
    @staticmethod
    def google_search(search_term, api_key, cse_id, **kwargs):
        company_url = 'Not found'
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        res = json.loads(json.dumps(res))
        # check if res['items'] exist
        try:
            if 'items' not in res:
                company_url = 'Not found'
            else:
                company_url=res['items'][0]['link']
        except Exception as e:
            company_url = 'Not found'
        return company_url
    @staticmethod
    def search_company(company_name):
        company_url = GoogleSearchService.google_search(f'{company_name}+問い合わせ', my_api_key, my_cse_id, num=10)
        print(f'company_url',company_url)
        return company_url
