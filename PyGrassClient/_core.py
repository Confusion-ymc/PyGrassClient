import json
import ssl
import sys
import threading
import time
import uuid
from urllib.parse import urlparse

import websocket
from faker import Faker
from loguru import logger

logger.remove()  # 移除默认的控制台输出处理器

logger.add(sys.stdout, level="INFO")  # 添加新的控制台输出处理器


def parse_proxy_url(proxy_url):
    parsed_url = urlparse(proxy_url)

    scheme = parsed_url.scheme
    host = parsed_url.hostname
    port = parsed_url.port
    auth = None

    if parsed_url.username and parsed_url.password:
        auth = (parsed_url.username, parsed_url.password)

    return scheme, host, port, auth


class PyGrassClient:
    def __init__(self, user_id, proxy_url=None):
        self.user_id = user_id
        self.user_agent = Faker().chrome()
        self.device_id = str(uuid.uuid4())
        self.ws = websocket.WebSocketApp(
            "wss://proxy.wynd.network:4650/",
            header=[
                f"User-Agent: {self.user_agent}"],
            on_error=self.on_error,
            on_message=self.on_message
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
                logger.error(f'ping error: {e}')

    def on_error(self, wsapp, err):
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
            logger.info(self.info("连接成功"))
        elif message.get("action") == "PONG":
            pong_response = {"id": message["id"], "origin_action": "PONG"}
            logger.debug(f'send {pong_response}')
            wsapp.send(json.dumps(pong_response))

    def run(self):
        if self.proxy_url:
            proxy_type, http_proxy_host, http_proxy_port, http_proxy_auth = parse_proxy_url(self.proxy_url)
        else:
            proxy_type = http_proxy_host = http_proxy_port = http_proxy_auth = None
        logger.info(self.info('Run start'))
        threading.Thread(target=self.send_ping, args=(self.ws,), daemon=True).start()
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, proxy_type=proxy_type, http_proxy_host=http_proxy_host,
                            http_proxy_port=http_proxy_port, http_proxy_auth=http_proxy_auth, reconnect=True)


def run_mult_acc(acc_file_path):
    with open(acc_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if "==" in line:
                account, proxy = line.split('==')
            else:
                account, proxy = line, None
            proxy = proxy or None
            threading.Thread(target=PyGrassClient(account, proxy).run, daemon=True).start()
    while True:
        time.sleep(1)