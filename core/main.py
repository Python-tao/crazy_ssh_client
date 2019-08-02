import os
import sys,threading
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)


from core import para_client
'''
主函数，生成了类的实例，运行了实例的交互函数。

'''

def run():

    para = para_client.ParaClient()
    # ftp.connect("192.168.88.128",9999)
    para.interactive()

