
import paramiko,threading
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import  settings
from core import server_file_reader

'''
ParaClient,集合了paramiko和threading两个模块，实现并发上传和下载。


'''

user_data = {
    'account_id':None,
    'is_authenticated':True,
    'current_dir':None,
    'account_data':None
}






class ParaClient(object):

    def __init__(self):
        '''
        down_file_path,实例变量，本地下载目录的绝对路径。

        '''
        self.down_file_path=settings.para_conf['down_file_path']
    def help(self):
        '''
        打印帮助文档的函数。
        '''
        msg = '''
使用方法：
batch_run -h h1,h2,h3 -cmd 'df -h'
batch_scp -h h1,h2,h3 -action put -local test.py -remote /tmp/
batch_scp -h h1,h2,h3 -action get -remote /tmp/test.py

bye
        '''
        print(msg)


    #运行远程命令的函数。
    def cmd_batch_run(self,*args):
        '''
        此函数，用于解析用户输入的batch_run开头的命令指令。主要有2个任务：
        一，根据输入的主机名获取主机的详细信息。
            主要通过server_file_reader.read_conf函数获取了主机清单文件中的主机信息。
        二，获取命令执行的指令，并向远程服务器发送该指令。
            1.使用多线程threading同时并发向多个后端服务器发送命令。
            2.执行命令使用para_cmd_run函数处理。

        '''
        cmd_split = args[0].split()
        if '-h' in cmd_split:
            h_name=cmd_split[cmd_split.index('-h')+1].split(',')
            host_data_list=[]
            for i in h_name:
                a,b,c,d=server_file_reader.read_conf(i)
                host_data_list.append({'hostname':a,'port':b,'username':c,'password':d})
            if '-cmd' in cmd_split:
                cmd_name=args[0].split('-cmd ')[1].strip('\'')
                t_objs = []
                for n in host_data_list:
                    # self.para_cmd_run(n,cmd_name)
                    t1=threading.Thread(target=self.para_cmd_run,args=(n,cmd_name,))
                    t1.start()
                    t_objs.append(t1)
                for t in t_objs:
                    t.join()

            else:
                self.help()


        elif '-g' in cmd_split:
            print("-g")
        else:
            self.help()



    def cmd_batch_scp(self, *args):
            '''
            cmd_batch_scp，文件上传下载的函数。
             此函数的作用：
            1.解析batch_scp命令，
            2.获取主机名，调用server_file_reader.read_conf函数读取主机清单文件，获取主机详细信息。
            3.根据命令的action类型使get还是put，分别进行处理。
              输入参数：
              batch_scp开头的命令，如 batch_scp -h h1,h2,h3 -action put -local test.py -remote /tmp/

            '''
            cmd_split = args[0].split()
            if '-h' and '-action' and '-local' and '-remote' in cmd_split:
                h_name = cmd_split[cmd_split.index('-h') + 1].split(',')
                host_data_list = []
                cmd_data_list = []
                for i in h_name:
                    a, b, c, d = server_file_reader.read_conf(i)
                    host_data_list.append({'hostname': a, \
                                           'port': b, \
                                           'username': c, \
                                           'password': d})
                cmd_type = cmd_split[cmd_split.index('-action') + 1]

                if cmd_type == 'put':
                    local_file_path = self.down_file_path + '/' +\
                                      cmd_split[cmd_split.index('-local') + 1]
                    if os.path.isfile(local_file_path):
                        remote_file_path = cmd_split[\
                                               cmd_split.index('-remote') + 1] \
                                           + '/' + cmd_split[
                            cmd_split.index('-local') + 1]
                        cmd_data_list.append(
                            {'cmd_type': cmd_type, \
                             'local_path': local_file_path, \
                             'remote_path': remote_file_path})
                        t_objs = []
                        for host_data in host_data_list:

                            t2 = threading.Thread(target=self.para_put_file,\
                                                  args=(host_data, cmd_data_list,))
                            t2.start()
                            t_objs.append(t2)
                        for t in t_objs:
                            t.join()
                    else:
                        print("文件：{},在本地目录并不存在。".format(local_file_path.split('/')[-1]))

                # batch_scp -h h1,h2,h3 -action get -remote /tmp/test.py
                elif cmd_type == 'get':
                    remote_file_path = cmd_split[cmd_split.index('-remote') + 1]
                    if remote_file_path.endswith('/'):
                        print("-->  {}  <--\nwrong remote file path!!".format(remote_file_path))
                    else:
                        t_objs = []
                        for host_data in host_data_list:
                            local_file_path = self.down_file_path + '/' + host_data[
                                'hostname'] + '.' + remote_file_path.split('/').pop(-1)
                            # self.para_get_file(host_data,remote_file_path,local_file_path)
                            t1 = threading.Thread(target=self.para_get_file,
                                                  args=(host_data, remote_file_path, local_file_path,))
                            t1.start()
                            t_objs.append(t1)
                        for t in t_objs:
                            t.join()



                else:
                    self.help()






            elif '-g' in cmd_split:
                print("-g is not ready.")

            else:
                self.help()


    def para_cmd_run(self,*args):
        '''
        调用paramiko运行远程命令模块
        此函数的作用：
            1.调用paramiko模块，连接远程主机。在远程服务器上执行命令。
            2.获取命令的执行结果，在本地主机上显示。

        输入参数：
            host_data,主机名，端口，用户名，密码等信息。
            cmd_data，需要在远程服务器上执行的命令。

        '''
        # 创建SSH对象
        host_data = args[0]
        cmd_data= args[1]
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=host_data['hostname'], \
                    port=host_data['port'], \
                    username=host_data['username'], \
                    password=host_data['password'])
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(cmd_data)
        # 获取命令结果
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        print("#############BEGIN###############")
        print("客户端：{}".format(host_data['hostname']))
        print(result.decode())
        print("##############END##############")
        print('\n')
        # 关闭连接
        ssh.close()




    def para_put_file(self,*args):
        '''
        paramiko上传文件模块,para_put_file
        作用:
            1.调用paramiko，连接远程服务器。
            2.执行上传命令，把文件上传到服务器。
        输入参数:
            host_data,服务器的详细信息。包括主机名，端口，用户名，密码。
            cmd_data，包括本地文件的绝对路径，远程服务器的文件绝对路径。

        '''
        host_data = args[0]
        cmd_data=args[1]
        transport = paramiko.Transport((host_data['hostname'], int(host_data['port'])))
        transport.connect(username=host_data['username'], password=host_data['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        # 将text.txt上传至服务器 /tmp/test_from_win
        print("####BEGIN####,正在把文件{},上传到服务器{}的{}。".format(cmd_data[0]['local_path'].split('/')[-1],host_data['hostname'],cmd_data[0]['remote_path']))
        sftp.put(cmd_data[0]['local_path'], cmd_data[0]['remote_path'])
        transport.close()



    def para_get_file(self,*args):
        '''
        paramiko下载文件模块:para_get_file
        作用:
            1.调用paramiko，连接远程服务器。
            2.执行下载命令，服务器上的文件下载到本地。
        输入参数:
            host_data,服务器的详细信息。包括主机名，端口，用户名，密码。
            remote_path，远程服务器的文件绝对路径。
            local_path，下载到本地的文件绝对路径。

        '''
        host_data=args[0]
        remote_path=args[1]
        local_path=args[2]
        transport = paramiko.Transport((host_data['hostname'],int(host_data['port'])))
        transport.connect(username=host_data['username'], \
                          password=host_data['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        # 将服务器的文件下载到本地 local_path
        print("####BEGIN####,正在从服务器{}把文件{},下载到本地{}".format(host_data['hostname'],remote_path,local_path.split('/')[-1]))
        sftp.get(remote_path, local_path)
        transport.close()




    def interactive(self):
        '''
        交互函数
        获取用户输入的命令字符串。
        通过反射获取对应的实例方法。
        然后运行该方法。

        '''
        print("你好，欢迎进入Crazy Para service sys，请输入你的命令。。")
        while user_data['is_authenticated'] is True:
            cmd = input(">>").strip()
            if len(cmd) ==0:continue
            cmd_str = cmd.split()[0]
            if hasattr(self,"cmd_%s" % cmd_str):
                func = getattr(self,"cmd_%s" % cmd_str)
                func(cmd)
            else:
                self.help()











