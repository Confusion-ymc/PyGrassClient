# Get Grass Python Package
[![PyPi Version](https://img.shields.io/pypi/v/PyGrassClient?color=green)](https://pypi.python.org/pypi/PyGrassClient/)
[![Build Sphinx docs)](https://github.com/Confusion-ymc/PyGrassClient/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Confusion-ymc/PyGrassClient/actions/workflows/python-publish.yml)


This is a python package for get grass score.

```
#!/usr/bin/env python

from PyGrassClient import PyGrassClient

PyGrassClient(user_id="${userid}", proxy_url='${proxy_url}').run()
```