import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)


from core import main


'''
paramiko service程序入口
'''

if __name__ == '__main__':
    main.run()