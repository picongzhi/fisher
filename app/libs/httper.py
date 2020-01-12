import json
from urllib import request

import requests


class HTTP(object):
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text

    @staticmethod
    def get_with_urllib(url, return_json=True):
        url = request.quote(url, safe='/:?=&')
        try:
            with request.urlopen(url) as r:
                result_str = str(r.read(), encoding='utf-8')
                return json.loads(result_str) if return_json else result_str
        except OSError as e:
            print(e.reason)
            return {} if return_json else ''
