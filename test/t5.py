# -*- coding:utf-8 -*-
# Author:lixuecheng


from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="读取可运行的脚本文件，需要.py结尾", metavar="FILE")
parser.add_option("-d", "--dir", dest="dir_name",
                  help="读取可以运行脚本的文件夹内所有符合要求的文件，输入值为指定文件夹", metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="不需要显示进度条和日志")

(options, args) = parser.parse_args()
print(options, args)

