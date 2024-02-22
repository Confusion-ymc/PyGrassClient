# Get Grass Python Package

This is a python package for get grass score.

```
#!/usr/bin/env python

from grass import GrassClient

GrassClient(user_id="${userid}", proxy_url='${proxy_url}').run()
```