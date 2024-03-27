import asyncio
import sys

from loguru import logger

from PyGrassClient import PyGrassClient
from PyGrassClient import run_by_file

# PyGrassClient(user_id="${userid}", proxy_url='${proxy_url}').run()
# run_by_file('accounts.txt')
logger.remove()  # 移除默认的控制台输出处理器

logger.add(sys.stdout, level="DEBUG")  # 添加新的控制台输出处理器

asyncio.run(PyGrassClient(user_id="5242367b-d366-4858-987a-9ebd303fa8f5", proxy_url='socks5://192.168.10.1:1070').connect_ws())