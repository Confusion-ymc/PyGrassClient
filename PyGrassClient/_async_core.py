import asyncio
import json
import ssl
import time
import uuid
from typing import Optional

import socks
import websockets
from faker import Faker
from loguru import logger
from websockets import WebSocketCommonProtocol

from PyGrassClient.utils import parse_proxy_url, Status


class AsyncGrassWs:
    def __init__(self, user_id, proxy_url=None):
        self.user_id = user_id
        self.user_agent = Faker().chrome()
        self.device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, proxy_url or ""))
        self.proxy_url = proxy_url
        self.ws: Optional[WebSocketCommonProtocol] = None
        self.status: Status = Status.disconnect
        self._stop = False
        self._stopped = False
        self._ping_stopped = False
        self.server_url = "wss://proxy.wynd.network:4650/"
        self.server_hostname = "proxy.wynd.network"

    async def send_ping(self):
        await asyncio.sleep(5)
        while not self._stop:
            try:
                send_message = json.dumps(
                    {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                if self.ws:
                    logger.debug(f'[发送消息] [{self.user_id}] [{self.proxy_url}] [{send_message}]')
                    await self.ws.send(send_message)
            except Exception as e:
                logger.debug(f'[PING Error] {e}')
            await asyncio.sleep(20)
        self._ping_stopped = True

    async def run(self):
        logger.info(f'[启动] [{self.user_id}] [{self.proxy_url}]')
        asyncio.create_task(self.send_ping())
        while True:
            try:
                self.status = Status.connecting
                if self.proxy_url:
                    proxy_type, http_proxy_host, http_proxy_port, http_proxy_auth = parse_proxy_url(self.proxy_url)
                    if http_proxy_auth:
                        username, password = http_proxy_auth[0], http_proxy_auth[1]
                    else:
                        username = password = None
                    # Initialize the connection to the server through the proxy
                    logger.debug(f'[连接代理] [{self.user_id}] [{self.proxy_url}]')
                    ws_proxy = socks.socksocket()
                    ws_proxy.set_proxy(socks.PROXY_TYPES[proxy_type.upper()], http_proxy_host, http_proxy_port,
                                       username=username, password=password)
                    ws_proxy.connect(("proxy.wynd.network", 4650))
                    logger.debug(f'[连接代理成功] [{self.user_id}] [{self.proxy_url}]')
                else:
                    ws_proxy = None
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                custom_headers = {
                    "User-Agent": self.user_agent
                }
                logger.debug(f'[连接服务器] [{self.user_id}] [{self.proxy_url}]')
                self.ws = await websockets.connect(
                    self.server_url,
                    ssl=ssl_context,
                    sock=ws_proxy,
                    extra_headers=custom_headers,
                    server_hostname=self.server_hostname,
                    open_timeout=60
                )

                logger.debug(f'[连接服务器成功] [{self.user_id}] [{self.proxy_url}]')
                while True:
                    response = await self.ws.recv()
                    message = json.loads(response)
                    logger.debug(f'[收到消息] [{self.user_id}] [{self.proxy_url}] [{message}]')
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
                        logger.debug(f'[发送消息] [{self.user_id}] [{self.proxy_url}] [{auth_response}]')
                        await self.ws.send(json.dumps(auth_response))
                        self.status = Status.connected
                        logger.info(f'[在线] [{self.user_id}] [{self.proxy_url}]')
                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(f'[发送消息] [{self.user_id}] [{self.proxy_url}] [{pong_response}]')
                        await self.ws.send(json.dumps(pong_response))
            except Exception as e:
                logger.debug(f'[连接断开] {e}')
            self.status = Status.disconnect
            if not self._stop:
                logger.debug(f'[重新连接] [{self.user_id}] [{self.proxy_url}]')
                await asyncio.sleep(5)
            else:
                while not self._ping_stopped:
                    await asyncio.sleep(1)
                logger.info(f'手动退出 [{self.user_id}] [{self.proxy_url}]')
                self._stopped = True
                break

    async def stop(self):
        self._stop = True
        if self.ws:
            await self.ws.close()

