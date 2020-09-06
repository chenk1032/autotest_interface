"""
HackerRank网站api相关测试
"""
from common import opmysql
import requests


class TestHackerRank:
    test_db = opmysql.OperationDbInterface()
    request_url = 'https://jsonmock.hackerrank.com/api/football_matches'

    # Todo: to be updated...
    def test_page_number(self):
        # 暂且把case_interface当作test case.简单测试，数据库其它字段待修改
        sen_sql = "select * from case_interface where id=2"
        expected_page_num = int(self.test_db.select_one(sen_sql)['data']['code_expect'])

        response = requests.get(self.request_url,
                                params={"year": 2011, "team1": 'Barcelona', "page": 1})
        actual_page_num = int(response.json()['page'])

        assert actual_page_num == expected_page_num

