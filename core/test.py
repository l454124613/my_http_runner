# -*- coding:utf-8 -*-
# Author:lixuecheng
from requests import request
import re

p = re.compile('<td><span>(.*?)</span></td>')
a = list()
for i in range(13):
    with request('post', 'http://shenfenzheng.293.net/like.php', data={'a': 'action'}) as r:
        # a.append()
        a.extend(p.findall(r.text))

for i in a:

    print(i)
