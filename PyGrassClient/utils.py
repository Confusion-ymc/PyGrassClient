from enum import Enum
from urllib.parse import urlparse

from requests import Session


class Status(Enum):
    disconnect = 0
    connecting = 1
    connected = 2


def parse_proxy_url(proxy_url):
    parsed_url = urlparse(proxy_url)

    scheme = parsed_url.scheme
    host = parsed_url.hostname
    port = parsed_url.port
    auth = None

    if parsed_url.username and parsed_url.password:
        auth = (parsed_url.username, parsed_url.password)

    return scheme, host, port, auth


def new_session(proxy_url=None):
    s = Session()
    s.headers = {
        'authority': 'api.getgrass.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://app.getgrass.io',
        'referer': 'https://app.getgrass.io/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }
    if proxy_url:
        s.proxies = {'http': proxy_url, "https": proxy_url}
    return s
