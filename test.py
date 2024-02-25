from PyGrassClient import PyGrassClient
from PyGrassClient import run_by_file

PyGrassClient(user_id="${userid}", proxy_url='${proxy_url}').run()
run_by_file('accounts.txt')