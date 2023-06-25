import requests
from common import utils,log

class RequestUtils():
    def __init__(self):
        self.log = log.Mylog()
        self.session = requests.session()
    #判断测试数据的完整性
    def standard_case_yaml(self,casedata:dict):
        '''
        校验yaml测试数据文件的完整性
        :param casedata: 测试数据路径
        :return:
        '''
        case_keys = casedata.keys()
        if "case_info" in case_keys and "requests" in case_keys:
            c_request = casedata['requests']
            c_req_keys = c_request.keys()
            if 'method' in c_req_keys and 'api' in c_req_keys and 'validate' in c_req_keys:
                val = c_request['validate']
                val_keys =  val.keys()
                if 'status_code' in val_keys and 'expected' in val_keys:
                    self.log.info('用例格式满足规定要求！')
                else:
                    self.log.error('用例缺少三级数据，status_code或者expected！')
            else:
                self.log.error('用例缺少二级数据，method、api或者validate！')

        else:
            self.log.error('用例缺少一级数据，case_info或者requests')

    def send_request(self,url:str,method:str,data=None,json=None,params=None,headers=None,files=None,**kwargs):
        '''

        :param url: 请求地址
        :param method: 请求方式
        :param data: data类型传参
        :param json: json类型请求参数
        :param params: url参数
        :param headers: 请求头头
        :param files:
        :param kwargs: 可变参数
        :return: Response
        '''
        try:
            res = self.session.request(url=url,method=method,data=data,json=json,headers=headers,params=params,files=files,**kwargs)
        except Exception as e:
            self.log.error('{}'.format(e))
        return res.status_code,res.json()