from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyA9feuXF6nAeh9fuTBT__gksb6doex_F88"
my_cse_id = "165a400ce7fe34dc1"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    print(res)
    return res['items']

results = google_search(
    '喫茶喫飯合同会社+問い合わせ', my_api_key, my_cse_id, num=10)

# Decode data
for result in results:
    if 'title' in result:
        result['title'] = result['title'].encode('latin1').decode('utf-8')
    if 'snippet' in result:
        result['snippet'] = result['snippet'].encode('latin1').decode('utf-8')
#save to json file
import json
with open('data.json', 'w',decode='utf-8') as f:
    json.dump(results, f)

for result in results:
    pprint.pprint(result)