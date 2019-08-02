# __author__ = "Alex Li"

import configparser #ConfigParser

config = configparser.ConfigParser()

config["DEFAULT"] = {'what': '11',
                     'where': '22',
                     'when': '33'}

config['h1'] = {}
config['h1']['hostname'] = '192.168.88.128'
config['h1']['port'] = '22'
config['h1']['username'] = 'root'
config['h1']['password'] = '123456'

config['h2'] = {}
config['h2']['hostname'] = '192.168.88.129'
config['h2']['port'] = '22'
config['h2']['username'] = 'root'
config['h2']['password'] = '123456'

config['h3'] = {}
config['h3']['hostname'] = '192.168.88.130'
config['h3']['port'] = '22'
config['h3']['username'] = 'root'
config['h3']['password'] = '123456'


with open('sample_host.ini', 'w') as configfile:
    config.write(configfile)


#原始版本
# import configparser  # ConfigParser
#
# config = configparser.ConfigParser()
#
# config["DEFAULT"] = {'ServerAliveInterval': '45',
#                      'Compression': 'yes',
#                      'CompressionLevel': '9'}
#
# config['h1'] = {}
# config['h1']['hostname'] = '192.168.88.128'
# config['h1']['port'] = '22'
# config['h1']['username'] = 'root'
# config['h1']['password'] = '123456'
#
# config['topsecret.server.com'] = {}
# config['topsecret.server.com']
# config['topsecret.server.com']['Host Port'] = '50022'  # mutates the parser
# config['topsecret.server.com']['ForwardX11'] = 'no'  # same here
#
# config['DEFAULT']['ForwardX11'] = 'yes'
#
# with open('example.ini', 'w') as configfile:
#     config.write(configfile)