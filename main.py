import requests
from requests.auth import HTTPBasicAuth
from opyml import OPML, Outline
import os
import json

output = 'site/nau-feeds-dynamic.opml.xml'
user = os.environ['API_USER']
key = os.environ['API_KEY']
basic = HTTPBasicAuth(user, key)

r = requests.get('https://nau.edu/cefns/wp-json/enterprise/v1/site-list', auth=basic)
r.encoding = r.apparent_encoding
dict = json.loads(r.text)

opml_doc = OPML()
global_rss_list = []
for i in dict:
    if i['url'][-1] == "/":
        url = i['url'][:-1]
    else:
        url = i['url']
    rss_url = f'https://{url}/rss'
    test = requests.get(rss_url)
    if test.status_code == 200:
        i['rss_url'] = rss_url
        i['rss_success'] = True
        opml_doc.body.outlines.append(Outline(text=f"NAU site: {i['name']}",
                                              type="rss",
                                              xml_url=i['rss_url'],
                                              html_url=i['url']
                                              ))
    else:
        i['rss_success'] = False
    global_rss_list.append(i)
    print(i)
print(global_rss_list)


with open(output, 'w') as w:
    w.write(opml_doc.to_xml())