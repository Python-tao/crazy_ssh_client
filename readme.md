# 主题：paramiko service

需求：
    使用paramiko封装了ssh客户端程序，提供命令行界面，支持向多台远程服务器并发发送命令并返回命令执行结果。
    支持同时向多台后端服务器并发文件上传和下载功能。

#命令行格式
## batch_run命令(已完成)
```
　　作用：向后端多个远程服务器发送命令，并返回命令的执行结果。
   格式：
        batch_run -h [HOST1,..] -cmd 'CMD_NAME'
            -h [HOST1,..],指明把命令发给后端哪个服务器，支持多个服务器。
            -cmd 'CMD_NAME'，指明执行的命令。支持Linux的管道符。
   示例：
        batch_run -h h1,h2,h3 -cmd 'df -h'

```


## batch_scp命令(已完成)
```
    作用:
        从后端多个服务器下载或者上传文件。
    格式：
        batch_scp -h [HOST1,..] -action [put/get] -local [File_Name] -remote [Dir_Name]
            -h [HOST1,..],指明把命令发给后端哪个服务器，支持多个服务器。
            -action [put/get],指明上传还是下载。
            -local [File_Name]，
                如果是上传文件，需要指明需要上传的文件名。
                如果是下载文件，则不需要指明。
            -remote [Dir_Name]，
                如果是上传文件，需要指明需要上传到远程服务器的哪个目录下，该目录必须首先存在。
                如果是下载文件，则需要指明需要下载的文件的绝对路径，不支持下载目录。
    示例：
        batch_scp -h h1,h2,h3 -action put -local test.py -remote /tmp/
        batch_scp -h h1,h2,h3 -action get -remote /tmp/test.py
        
        
```




# 主机清单sample_host.ini结构：
```
    [hi]        主机别名
    hostname    主机ip
    port        ssh服务的端口
    username    服务器端的用户名
    password    服务器端的密码
```

# 使用的模块
```
    configparser，  用于解析ini风格的配置文件。
    paramiko        连接远程服务器的ssh服务。
    threading       多线程模块
    
```



# 目录结构
```
- bin 
    -run_para.py          程序启动入口
- conf
    -settinggs.py           全局配置文件，保存了本地下载路径。
    -sample_host.ini        服务器主机清单文件
    -configparser_creat_ini_file.py 创建ini格式的主机清单文件的模块
    -configparser_read_ini_file.py  读取ini格式的主机清单文件的模块
    
-core                        核心代码
    -main.py                主函数.
    -para_client.py            使用类封装了客户端的各种功能。
    -server_file_reader.py      读取主机清单文件的模块
-data                           本地下载文件目录


readme.md                       readme文件
```