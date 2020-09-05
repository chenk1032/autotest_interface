from common import opmysql


class TestSql:

    def test_insert_data(self):
        test_db = opmysql.OperationDbInterface()
        result = test_db.insert_data("insert into case_interface("
                                     "name_interface,"
                                     "exe_mode,"
                                     "url_interface,"
                                     "header_interface,"
                                     "params_interface,"
                                     "result_interface,"
                                     "code_to_compare,"
                                     "code_expect,"
                                     "params_to_compare,"
                                     "params_actual) "
                                     "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                     [('HackerRank_football', 'get',
                                      'https://jsonmock.hackerrank.com/api/football_matches', 'temp',
                                      'year=2011&team1=Barcelona&page=1', 'temp', 'code', '200', 'page', 'temp')])
        print(result['message'])
