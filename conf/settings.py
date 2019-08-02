# __author__ = "XYT"

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

'''
全局配置文件
    down_file_path，本地的下载目录的绝对路径。
    host_file_path，主机清单文件sample_host.ini的绝对路径。

'''


para_conf = {
    'engine': 'file_storage',  # support mysql,postgresql in the future
    'name': 'accounts',
    'down_file_path': "%s/data" % BASE_DIR,
    'host_file_path':"%s/conf/sample_host.ini" % BASE_DIR

}




