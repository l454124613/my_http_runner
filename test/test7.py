# -*- coding:utf-8 -*-
# Author:lixuecheng
import os, sys
from core.Request import Request

index = None
directory = os.getcwd()
added_to_path = False
file_name = 't6.py'
abs_file = os.path.join(directory, file_name)
if os.path.exists(abs_file):
    pass

else:
    print('文件%s，不存在' % abs_file)
if directory not in sys.path:
    sys.path.insert(0, directory)
    added_to_path = True
# If the directory IS in the PYTHONPATH, move it to the front temporarily,
# otherwise other locustfiles -- like Locusts's own -- may scoop the intended
# one.
else:
    i = sys.path.index(directory)
    if i != 0:
        # Store index for later restoration
        index = i
        # Add to front, then remove from original position
        sys.path.insert(0, directory)
        del sys.path[i + 1]
# Perform the import (trimming off the .py)
sys.path.append('wei_le_pi_liang_yun_xing')
imported = __import__('t6')
sys.path.remove('wei_le_pi_liang_yun_xing')
# Remove directory from path if we added it ourselves (just to be neat)
if added_to_path:
    del sys.path[0]
# Put back in original index if we moved it
if index is not None:
    sys.path.insert(index + 1, directory)
    del sys.path[0]


def is_locust(tup):
    """
    Takes (name, object) tuple, returns True if it's a public Locust subclass.
    """
    name, item = tup
    import inspect
    return bool(

        inspect.isclass(item)
        and issubclass(item, Request)
        and hasattr(item, "ff")
        # and getattr(item, "ff")
        and not name == 'Request'
        and not name.startswith('_')
        # and item  is not  Request
    )


# print(vars(imported).items())
locusts = dict(filter(is_locust, vars(imported).items()))
vv = list(locusts.values())[0]
vv2=vv()
ll = getattr(vv2, 'ff')
for n in ll:
    getattr(vv2,n)()
print(getattr(vv2, 'ff'))
# print(locusts)
# cl = [locusts[n] for n in locusts.keys()]

# print(dir(list(locusts.values())[0]))
# print(locusts.items())
# print(vars(imported).items())
