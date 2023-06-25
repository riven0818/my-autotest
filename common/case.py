from common import log,utils,requests,asserts
import os


class Case():
    def __init__(self):
        self.log = log.Mylog()
        self.req = requests.RequestUtils()
        self.art = asserts.Asserts()

    def run_case(self,case_data_path):
        '''执行用例

        :param case_data_path: 用例数据
        :return: None
        '''
        #获取文件测试数据并检查数据文件，是否符合模板规则,res是字典列表
        self.res = utils.readyaml(f_path=case_data_path)
        print('\n')
        self.log.info('-----------------开始用例数据格式校验--------------')
        for i in range(len(self.res)):
            if 'case_info' in self.res[i].keys() and "requests" in self.res[i].keys():
                if 'method' in self.res[i]['requests'].keys() and 'api' in self.res[i]['requests'].keys() and 'validate' in self.res[i]['requests'].keys():
                    if 'status_code' in self.res[i]['requests']['validate'].keys() and 'expected' in self.res[i]['requests']['validate'].keys():
                        self.log.info('校验结果：用例格式满足要求')
                    else:
                        self.log.error('校验结果：缺少stutus_code或者expected键')
                        raise KeyError
                        break
                else:
                    self.log.error('校验结果：缺少method、api或者validate键')
                    raise KeyError
                    break
            else:
                self.log.error('校验结果：缺少case_info或者requests键')
                raise KeyError
                break
        #公用数据提取
        self.log.info('-------------------用例数据准备------------------')
        for i in range(len(self.res)):
            method = self.res[i]['requests']['method']
            api = self.res[i]['requests']['api']
            if 'data' not in self.res[i]['requests']:
                data = None
            else:
                data = self.res[i]['requests']['data']
            if 'json' not in self.res[i]['requests']:
                json = None
            else:
                json = self.res[i]['requests']['json']

            if 'params' not in self.res[i]['requests']:
                params = None
            else:
                params = self.res[i]['requests']['params']
            if 'headers' not in self.res[i]['requests']:
                headers = None
            else:
                headers = self.res[i]['requests']['headers']
            if 'files' not in self.res[i]['requests']:
                files = None
            else:
                files = self.res[i]['requests']['files']

            status_code = self.res[i]['requests']['validate']['status_code']
            expected = self.res[i]['requests']['validate']['expected']
            url = utils.readyaml(f_path=(os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\','/') + '/config/env.yaml'))['host'] + api

            # 运行用例请求,并对结果进行判断
            if self.res[i]['requests']['req_method'] == 'request':
                self.log.info('用例{}:开始执行'.format(i+1))
                result = self.req.send_request(url=url, method=method,data=data,json=json,params=params,headers=headers,files=files)
                self.log.info('预期结果：{}'.format(expected))
                self.log.info('实际结果：{}'.format(result))
                #断言方式
                art = str(self.res[i]['requests']['assert_type'])
                if status_code == result[0]:
                    self.log.info('校验1：实际请求响应状态码和预期状态码一致，status_code:{}'.format(result[0]))
                    if art.lower() == 'expected_in_actual':
                        res_art = self.art.assert_in(actual=result[1],expected_msg=expected)
                        if res_art == 'EXPECT_IN_ACTUAL':
                            self.log.info('校验2：实际结果包含预期结果,用例通过！')
                        else:
                            self.log.error("校验2：实际结果不包含预期结果或者值不相等，用例不通过！")
                    #其他断言方式
                    else:
                        self.log.warning('其他的断言方式，请在assert.py里补充')
                else:
                    self.log.error('status_code错误!请检查！status_code:{}，result:{}'.format(status_code,result[0]))
            else:
                self.log.warning('其他请求方法请补充')

