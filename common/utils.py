import yaml
import os
from configparser import ConfigParser

def readyaml(f_path):
    r'''
    读取yaml文件内容
    :param f_path: 数据文件路径，包括文件名称
    :return:
    '''
    with open(f_path,mode='r',encoding='utf-8') as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
    return data

def wirteyaml(f_path,w_data):
    '''
    将数据文件写入yaml文件
    :param f_path: 文件路径，包括即将写入的空文件名称
    :param w_data: 写入的文件数据
    :return:
    '''
    with open(f_path,'w',encoding='utf-8') as f:
        yaml.dump(w_data,stream=f)

def removefile(dir_path):
    os.removedirs(dir_path)

def confparams(file_name,section,key):
    '''
    获取配置中的数据
    :param file_name: 配置文件路径，包括文件名称
    :param section: 配置文件中的部件名
    :param key: 配置文件中变量名
    :return:
    '''
    conf = ConfigParser()
    conf.read(filenames=file_name,encoding='utf-8')
    res = conf.get(section=section,option=str(key),raw=True)
    return res


#logger_path用于logging中__init__方法中的os.path.normcase()
logger_path = os.path.dirname(os.path.abspath(__file__)) + '\log.py'
