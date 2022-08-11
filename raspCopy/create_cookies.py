import requests
import json

data = {
    'f_login': 'admin',
    'f_password': 'Zajr}/#t%p{A'
}

link = 'http://172.16.10.131/main.php?p=login'
session = requests.Session()
responce = session.post(link, data=data).text
cookies_dict = [
    {"domain":key.domain, "name":key.name, "path":key.path, "value":key.value}
    for key in session.cookies
]

with open('cookies.json', 'w') as file:
    json.dump(cookies_dict, file, indent=4, ensure_ascii=False)
