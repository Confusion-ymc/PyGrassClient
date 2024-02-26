import json
import ssl
import sys
import threading
import time
import uuid

import websocket
from faker import Faker
from loguru import logger
from websocket import setdefaulttimeout

from PyGrassClient.utils import parse_proxy_url, new_session

logger.remove()  # 移除默认的控制台输出处理器

logger.add(sys.stdout, level="INFO")  # 添加新的控制台输出处理器


class GrassWs:
    def __init__(self, user_id, proxy_url=None):
        self.user_id = user_id
        self.is_online = False
        self.reconnect_times = 0
        self.user_agent = Faker().chrome()
        self.device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, proxy_url or ""))
        self.ws = websocket.WebSocketApp(
            "wss://proxy.wynd.network:4650/",
            header=[
                f"User-Agent: {self.user_agent}"],
            on_error=self.on_error,
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close
        )
        self.proxy_url = proxy_url

    def info(self, message):
        return f'\n------\n[{message}]\n[user_id: {self.user_id}]\n[proxy_url: {self.proxy_url}]\n[device_id: {self.device_id}]\n------\n'

    def send_ping(self, wsapp):
        while True:
            time.sleep(20)
            try:
                send_message = json.dumps(
                    {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                wsapp.send(send_message)
                logger.debug(f'send {send_message}')
            except Exception as e:
                logger.error(f'[user_id: {self.user_id}] [proxy_url: {self.proxy_url}] ping error: {e}')

    def on_open(self, wsapp):
        self.reconnect_times += 1

    def on_close(self, wsapp, close_status_code, close_msg):
        self.is_online = False
        logger.error(self.info(f'Connect close: {close_msg}'))

    def on_error(self, wsapp, err):
        self.is_online = False
        logger.error(self.info(f'Connect error: {err}'))

    def on_message(self, wsapp, message):
        message = json.loads(message)
        logger.debug(f'recv {message}')
        if message.get("action") == "AUTH":
            auth_response = {
                "id": message["id"],
                "origin_action": "AUTH",
                "result": {
                    "browser_id": self.device_id,
                    "user_id": self.user_id,
                    "user_agent": self.user_agent,
                    "timestamp": int(time.time()),
                    "device_type": "extension",
                    "version": "3.3.0"
                }
            }
            logger.debug(f'send {auth_response}')
            wsapp.send(json.dumps(auth_response))
            self.is_online = True
            logger.info(self.info(f"连接成功 连接次数: {self.reconnect_times}"))
        elif message.get("action") == "PONG":
            pong_response = {"id": message["id"], "origin_action": "PONG"}
            logger.debug(f'send {pong_response}')
            wsapp.send(json.dumps(pong_response))

    def run(self):
        setdefaulttimeout(30)
        if self.proxy_url:
            proxy_type, http_proxy_host, http_proxy_port, http_proxy_auth = parse_proxy_url(self.proxy_url)
        else:
            proxy_type = http_proxy_host = http_proxy_port = http_proxy_auth = None
        logger.info(self.info('Run start'))
        threading.Thread(target=self.send_ping, args=(self.ws,), daemon=True).start()
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, proxy_type=proxy_type, http_proxy_host=http_proxy_host,
                            http_proxy_port=http_proxy_port, http_proxy_auth=http_proxy_auth, reconnect=True)


class PyGrassClient:
    def __init__(self, *, user_name=None, password=None, user_id=None, proxy_url=None):
        assert user_id or (user_name and password), Exception('must set user_name and password or set user_id!')
        self.user_name = user_name
        self.password = password
        self.user_id = user_id
        self.proxy_url = proxy_url
        self.session = new_session(self.proxy_url)
        self.ws = GrassWs(self.user_id, self.proxy_url)
        self.is_login = False

    def login(self):
        assert (self.user_name and self.password), Exception('must set user_name and password!')
        json_data = {
            'user': self.user_name,
            'password': self.password,
        }
        response = self.session.post('https://api.getgrass.io/auth/login', json=json_data).json()
        if response["status"] == "success":
            self.user_id = response["data"]["id"]
            self.is_login = True
        else:
            raise Exception(f'login fail, [{self.user_name}, {self.password}]')

    def get_dash(self):
        response = self.session.get('https://api.getgrass.io/users/dash').json()
        # print(sum([item['earning'] for item in response['data']['devices']]))
        return response

    def connect_ws(self):
        if not self.user_id:
            self.login()
        self.ws.user_id = self.user_id
        self.ws.run()


def run_by_file(acc_file_path):
    all_clients = load_account_by_file(acc_file_path)
    for client in all_clients:
        threading.Thread(target=client.connect_ws, daemon=True).start()
    while True:
        logger.info(f'online: {len(list(filter(lambda x: x.ws.is_online, all_clients)))} all: {len(all_clients)}')
        time.sleep(10)


def load_account_by_file(acc_file_path):
    all_clients = []
    index = 0
    with open(acc_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "==" in line:
                user_id, proxy_url = line.split('==')
            else:
                user_id, proxy_url = line, None
            if "---" in user_id:
                user_name, password = user_id.split('---')
            else:
                user_name = password = None
            proxy_url = proxy_url or None
            index += 1
            client = PyGrassClient(user_id=user_id, user_name=user_name, password=password, proxy_url=proxy_url)
            logger.info(f'[{index}] [user_id: {user_id}] [proxy: {proxy_url}]')
            all_clients.append(client)
    return all_clients
