# Get Grass Python Package
[![PyPi Version](https://img.shields.io/pypi/v/PyGrassClient?color=green)](https://pypi.python.org/pypi/PyGrassClient/)
[![Build Sphinx docs)](https://github.com/Confusion-ymc/PyGrassClient/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Confusion-ymc/PyGrassClient/actions/workflows/python-publish.yml)

**This is a python package for get grass score.**

## 1. 安装
```
pip3 install PyGrassClient
```
## 2. 使用
### **1. 单账号运行**
 ```
 #!/usr/bin/env python
 
 from PyGrassClient import PyGrassClient
 
 PyGrassClient(user_id="${userid}", proxy_url='${proxy_url}').run()
 ```
### **2. 多账号运行**
 ```
 #!/usr/bin/env python
 
 from PyGrassClient import run_by_file
 
 run_by_file('accounts.txt')
 ```

### **3. Docker运行**
 
1. `git clone https://github.com/Confusion-ymc/PyGrassClient.git`
2. 添加`account.txt`文件
3. `docker compose up --build -d`

### 4. account.txt 文件格式 
#### **每一行是一个账号,如果使用代理则在后面加上`==代理连接`, 没有代理则直接是`user_id`为一行** 
 ```text
 5242367b-d366-1234-987a-9ebd303fa8f5==http://proxy.com:8080
 5242367b-d366-1234-987a-9ebd303fa8f5
 5242367b-d366-1258-987a-9ebd303fa8f5==socks5://proxy.com:1080
 ```