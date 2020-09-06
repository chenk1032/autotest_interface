"""
数据库连接和操作的测试
"""
from common import opmysql


class TestSql:
    test_db = opmysql.OperationDbInterface()
    api_url = 'https://jsonmock.hackerrank.com/api/football_matches'

    def test_insert_data(self):
        """
        向表case_interface添加记录，为添加一条api测试用例
        :return: assert 添加成功
        """
        sql_insert = "INSERT INTO case_interface(" \
                     "name_interface,exe_mode,url_interface,header_interface,params_interface,result_interface," \
                     "code_to_compare,code_expect, params_to_compare, params_actual) " \
                     "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result = self.test_db.insert_data(sql_insert,
                                          [('HackerRank_football', 'get', self.api_url, 'temp',
                                            'year=2011&team1=Barcelona&page=1', 'temp', 'code', '200', 'page', 'temp')])
        assert result['code'] == '0000'
