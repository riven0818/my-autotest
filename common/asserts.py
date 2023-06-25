from common import requests,log
logger = log.Mylog()

class Asserts():
    def __init__(self):
        pass

    def assert_body(self,body,body_msg,expected_msg):
        '''
        判断请求的body体任意属性的值
        :param body: 请求返回值
        :param body_msg: 任意属性值,多层级需指定到最小
        :param expected_msg: 预期属性值
        :return:
        '''
        try:
            assert body[body_msg] == expected_msg
            logger.info('body中属性值和预期属性值箱等')
            return True
        except:
            logger.error('body中查看的属性值和预期属性值不等，不通过')
            raise
    def assert_in(self,actual:dict,expected_msg:dict):
        '''
        判断返回值是否包含预期结果
        :param body: 请求返回值
        :param expected_msg: 预期结果
        :return:
        '''
        try:
            for key in expected_msg.keys():
                if expected_msg[key] == actual[key]:
                    return 'EXPECT_IN_ACTUAL'
                else:
                    return "EXPECT_NOTIN_ACTUAL"
        except Exception as e:
            logger.error(e)
