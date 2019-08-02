#Author:xyt
import configparser
import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)

from conf import settings
'''
server_file_path,本地主机清单文件sample_host.ini的绝对路径。
read_conf函数的作用：
    1.调用configparse模块，读取ini风格的配置文件的内容。
    2.返回相应的文件信息给调用者。
        包括主机名，主机端口，用户名和用户密码。


'''



server_file_path=settings.para_conf['host_file_path']




def read_conf(target_host):
    conf = configparser.ConfigParser()
    conf.read(server_file_path)
    return conf[target_host]['hostname'],conf[target_host]['port'],conf[target_host]['username'],conf[target_host]['password']




# a,b,c,d=read_conf('h1')
#
# print(a)
# print(b)
# print(c)
# print(d)
