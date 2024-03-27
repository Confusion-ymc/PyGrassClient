import sys

from loguru import logger

from PyGrassClient import run_by_file

logger.remove()  # 移除默认的控制台输出处理器

logger.add(sys.stdout, level="INFO")  # 添加新的控制台输出处理器

run_by_file('accounts.txt')
