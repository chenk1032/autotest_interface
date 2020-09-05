"""
定义数据比较方法
compare_param 对外的参数比较类
compare_code 关键参数值比较方法
compare_params_complete参数完整性比较
get_compare_params 获得返回包数据去重集合
recur_params 递归操作，辅助去重
"""

import json
import logging

from common import opmysql
from public import config

operation_db = opmysql.OperationDbInterface()


class CompareParam(object):
    def __init__(self, params_interface):
        self.params_interface = params_interface
        self.id_case = params_interface['id']
        self.result_list_response = []
        self.params_to_compare = params_interface['params_to_compare']

    def compare_code(self, result_interface):
        """
        关键参数值code比较
        :param result_interface: 返回包数据
        :return: 返回码code 返回信息message 数据data
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)
                temp_code_to_compare = self.params_interface['code_to_compare']
                if temp_code_to_compare in temp_result_interface.keys():
                    if str(temp_result_interface[temp_code_to_compare]) == str(self.params_interface['code_expect']):
                        result = {'code': '0000', 'message': '关键字参数值相同', 'data': []}
                        operation_db.op_sql("update case_interface "
                                            "set code_actual='%s', result_code_compare=%s "
                                            "where id=%s "
                                            % (temp_result_interface[temp_code_to_compare], 1, self.id_case))
                    elif str(temp_result_interface[temp_code_to_compare]) != str(self.params_interface['code_expect']):
                        result = {'code': '1003', 'message': '关键字参数值不相同', 'data': []}
                        operation_db.op_sql("update case_interface "
                                            "set code_actual='%s', result_code_compare=%s "
                                            "where id=%s  "
                                            % (temp_result_interface[temp_code_to_compare], 0, self.id_case))
                    else:
                        result = {'code': '1002', 'message': '关键字参数值比较出错', 'data': []}
                        operation_db.op_sql("update case_interface "
                                            "set code_actual='%s', result_code_compare=%s "
                                            "where id=%s "
                                            % (temp_result_interface[temp_code_to_compare], 3, self.id_case))
                else:
                    result = {'code': '1001', 'message': '返回包数据无关键字参数', 'data': []}
                    operation_db.op_sql("update case_interface "
                                        "set result_code_compare=%s "
                                        "where id=%s "
                                        % (2, self.id_case))
            else:
                result = {'code': '1000', 'message': '返回包格式不合法', 'data': []}
                operation_db.op_sql("update case_interface "
                                    "set result_code_compare=%s "
                                    "where id=%s "
                                    % (4, self.id_case))
        except Exception as error:
            result = {'code': '9999', 'message': '关键字参数比较异常', 'data': []}
            operation_db.op_sql("update case_interface "
                                "set result_code_compare=%s "
                                "where id=%s "
                                % (9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result

    def get_compare_params(self, result_interface):
        """
        将接口返回数据中的参数名写入列表中
        :param result_interface: 返回包数据
        :return: 返回码code,返回信息.message 数据data
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)
                self.result_list_response = temp_result_interface.keys()
                result = {'code': '0000', 'message': '成功', 'data': self.result_list_response}
            else:
                result = {'code': '1000', 'message': '返回包格式不合法', 'data': []}
        except Exception as error:
            result = {'code': '9999', 'message': '数据处理异常', 'data': []}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result

    def compare_params_complete(self, result_interface):
        """
        参数完整性比较，比较参数值与__cur_params()返回的结果
        :param result_interface:
        :return:
        """
        try:
            temp_compare_params = self.__recur_params(result_interface)
            if temp_compare_params['code'] == '0000':
                temp_result_list_response = temp_compare_params['data']
                if self.params_to_compare.startswith('[') and isinstance(self.params_to_compare.str):
                    list_params_to_compare = eval(self.params_to_compare)
                    if set(list_params_to_compare).issubset(set(temp_result_list_response)):
                        result = {'code': '0000', 'message': '参数完整性比较一致', 'data': []}
                        operation_db.op_sql('update case_interface '
                                            'set params_actual="%s", result_params=%s '
                                            'where id="%s"'
                                            % (temp_result_list_response, 1, self.id_case))
                    else:
                        result = {'code': '3001', 'message': '实际结果中元素不都在预期结果中', 'data': []}
                        operation_db.op_sql('update case_interface '
                                            'set params_actual="%s", result_params=%s '
                                            'where id="%s"'
                                            % (temp_result_list_response, 0, self.id_case))
                else:
                    result = {'code': '4001', 'message': '用例中待比较参数集错误', 'data': self.params_to_compare}
            else:
                result = {'code': '2001', 'message': '调用__recur_params返回错误', 'data': []}
                operation_db.op_sql('update case_interface '
                                    'set result_params_compare=%s '
                                    'where id="%s"'
                                    % (2, self.id_case))
        except Exception as error:
            result = {'code': '9999', 'message': '参数完整性比较异常', 'data': []}
            operation_db.op_sql('update case_interface '
                                'set result_params_compare=%s '
                                'where id="%s"'
                                % (9, self.id_case))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        finally:
            return result

    def __recur_params(self, result_interface):
        """
        递归方法
        :param result_interface:
        :return:
        """
        try:
            if result_interface.startswith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)
                self.__recur_params(temp_result_interface)
            elif isinstance(result_interface, dict):
                for param, value in result_interface.items():
                    self.result_list_response.append(param)
                    if isinstance(value, list):
                        for param in value:
                            self.__recur_params(param)
                    elif isinstance(value, dict):
                        self.__recur_params(value)
                    else:
                        continue
                else:
                    pass
        except Exception as error:
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
            return {'code': '9999', 'message': '处理数据异常', 'data': []}
        return {'code': '0000', 'message': '成功', 'data': list(set(self.result_list_response))}


if __name__ == "__main__":
    sen_sql = "select * from case_interface where name_interface='getIpInfo.php' and id=1"
    params_interface = operation_db.select_one(sen_sql)
    result_interface = params_interface['data']['result_interface']
    test_compare_param = CompareParam(params_interface['data'])
    result_compare_code = test_compare_param.compare_code(result_interface)
    print(result_compare_code)
    result_compare_params_complete = test_compare_param.compare_params_complete(result_interface)
    print(result_compare_params_complete)
