# -*- coding:utf-8 -*-
# Author:lixuecheng
from enum import Enum, unique


@unique
class ResponseItem(Enum):
    json = 1
    content = 2
    status_code = 3
    encoding = 4
    headers = 5
    cookies = 6
