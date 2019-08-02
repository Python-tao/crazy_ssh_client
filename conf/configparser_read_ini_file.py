
'''
读取配置文件
conf,导入模块后,生成一个对象.
conf.read("example.ini")
    调用read方法,传入配置文件.
conf.defaults(),获取默认配置段.
conf.sections(),获取分段配置段.
conf['bitbucket.org']['user'],获取指定配置段中指定项目的值.
conf.remove_section('bitbucket.org'),
    调用remove_section方法,删除某个配置段.
conf.write(open('example.ini', "w"))
    调用write方法,保存文件.

'''




import configparser

conf = configparser.ConfigParser()
conf.read("sample_host.ini")

print(conf['h1']['hostname'])
print(conf.sections())
# sec = conf.remove_section('bitbucket.org')

# conf.remove_section('bitbucket.org')
# conf.write(open('example.ini', "w"))





#原始版本
# import configparser
#
# conf = configparser.ConfigParser()
# conf.read("sample_host.ini")
#
# print(conf.defaults())
#
# print(conf['bitbucket.org']['user'])
# print(conf.sections())
# sec = conf.remove_section('bitbucket.org')

# conf.remove_section('bitbucket.org')
# conf.write(open('example.ini', "w"))