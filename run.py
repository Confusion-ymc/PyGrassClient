import os

from PyGrassClient import PyGrassClient

PyGrassClient(user_id=os.getenv('USER_ID'), proxy_url=os.getenv('PROXY_URL')).run()
