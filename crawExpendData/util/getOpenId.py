import json

import requests


def getOpenId(token):
    headers = {
        'Authorization': token
    }
    result = requests.get("http://127.0.0.1/Bookkeeping/api/getOpenId", headers=headers, data="DjangoAccess")
    result = json.loads(result.text)
    print(result['data'])
    return result['data']
