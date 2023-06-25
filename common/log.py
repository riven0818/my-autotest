import logging
import colorlog
import os
from os import path
from common import utils
import time

#获取当前文件路径
cur_path = path.dirname(path.dirname(path.abspath(__file__))).replace('\\','/') + '/config/env.yaml'

#生成日志文件名称
log_file_name = 'pytest_' + time.strftime('%Y-%m-%d') + '.log'
log_errfile_name = 'pytest_' + time.strftime('%Y-%m-%d') + '_err.log'

#生成日志目录
if not path.exists(path.join(path.dirname(path.dirname(path.abspath(__file__))).replace('\\','/'),'log')):
    os.mkdir(path.join(path.dirname(path.dirname(path.abspath(__file__))).replace('\\','/'),'log'))


class Mylog():
    def __init__(self):
        self.log_stats = utils.readyaml(f_path=cur_path)
        self.log_file_level = self.log_stats['log']['log_file_level']
        self.log_console_level = self.log_stats['log']['log_console_level']
        self.log_file_format = self.log_stats['log']['log_file_format']
        self.log_console_format = self.log_stats['log']['log_console_format']
        self.log_color = self.log_stats['log']['log_console_typeface_color']

        #日志文件名称
        self.log_name = path.dirname(path.dirname(path.abspath(__file__))).replace('\\','/') + '/log/' + log_file_name
        self.errlog_name = path.dirname(path.dirname(path.abspath(__file__))).replace('\\','/') + '/log/' + log_errfile_name
        #生成日志器
        self.logger = logging.getLogger(__name__)
        #设置日志器的默认等级
        if self.log_stats['log']['logger_default_level'] not in (self.log_stats['log']) or \
                self.log_stats['log']['logger_default_level'] == '':
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(self.log_stats['log']['logger_default_level'])

    def __handler(self,level,message):
        #创建filehandler写到本地日志文件
        '''????为什么mode为w时，日志文件只生成critical那条日志'''
        fh = logging.FileHandler(self.log_name,mode='a',encoding='utf-8')
        #设置文件日志器的日志级别
        fh.setLevel(self.log_file_level)
        #设置日志器文件格式
        log_file_format = logging.Formatter(self.log_file_format,datefmt='%Y-%m-%d  %H:%M:%S')
        #log_file_format = colorlog.ColoredFormatter(fmt=self.log_file_format,log_colors=self.log_color,datefmt='%Y-%m-%d  %H:%M:%S')
        fh.setFormatter(fmt=log_file_format)
        #添加修改后的配置
        self.logger.addHandler(fh)


        #错误日志处理器
        eh = logging.FileHandler(self.errlog_name,mode='a',encoding='utf-8')
        eh.setLevel(logging.ERROR)
        eh.setFormatter(fmt=log_file_format)
        self.logger.addHandler(eh)

        #控制台处理器
        ch = logging.StreamHandler()
        ch.setLevel(self.log_console_level)
        console_color_format = colorlog.ColoredFormatter(fmt=self.log_console_format,log_colors=self.log_color,datefmt='%Y-%m-%d  %H:%M:%S')
        ch.setFormatter(console_color_format)
        self.logger.addHandler(ch)

        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)
        else:
            raise '日志级别错误'

        #重复日志处理
        self.logger.removeHandler(fh)
        self.logger.removeHandler(ch)
        self.logger.removeHandler(eh)
        #关闭文件
        fh.close()
        eh.close()
        
    def debug(self,message):
        self.__handler('debug',message)

    def info(self,message):
        self.__handler('info',message)

    def warning(self,message):
        self.__handler('warning',message)

    def error(self,message):
        self.__handler('error',message)

    def critical(self,message):
        self.__handler('critical',message)


if __name__ == '__main__':
    Log = Mylog()
    Log.debug("this is a debug level message")
    Log.info('this is a info level message')
    Log.warning('this is a warning level message')
    Log.error('this is a error level message')
    Log.critical('this is a critical message')