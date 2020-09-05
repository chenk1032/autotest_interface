# -*- coding:utf-8 -*-
# __author__ = 'cxx copy from ...'
"""
MySql基本操作封装
"""
import logging
import os
import pymysql

from public import config

ath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class OperationDbInterface(object):
    # link_type 返回数据格式 0=字典 !0=元组
    def __init__(self, host_db='127.0.0.1', user_db='test_user1', passwd_db='test_user1', name_db='test_interface',
                 port_db=3306, link_type=0):
        try:
            if link_type == 0:
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            else:
                self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                            charset='utf8')
            self.cur = self.conn.cursor()
            print("数据库连接成功")
        except pymysql.Error as e:
            print("创建数据库连接失败 | Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)

    def op_sql(self, condition):
        """
        :param condition: 通用操作SQL语句，可替代update_one, delete_one
        :return: 字典格式
        """
        try:
            self.cur.execute(condition)
            self.conn.commit()
            result = {'code': '0000', 'message': '执行通用操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行通用操作异常', 'data': []}
            print("数据库错误|op_sql %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def select_one(self, condition):
        """
        :param condition: 查询语句
        :return: 查询结果字典{'code': '0000/9999'成功/失败, 'message': '执行单条查询操作成功', 'data': results}
        """
        try:
            rows_affect = self.cur.execute(condition)
            # 查询到
            if rows_affect > 0:
                results = self.cur.fetchone()
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': results}
            # 未查询到（查询操作成功）
            else:
                result = {'code': '0000', 'message': '执行单条查询操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行单条查询操作异常', 'data': []}
            print("数据库错误|select_one %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def select_all(self, condition):
        try:
            rows_affect = self.cur.execute(condition)
            # 查询到
            if rows_affect > 0:
                self.cur.scroll(0, mode='absolute')  # 将游标置初始位置
                results = self.cur.fetchall()
                result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': results}
            # 未查询到（查询操作成功）
            else:
                result = {'code': '0000', 'message': '执行批量查询操作成功', 'data': []}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行批量查询操作异常', 'data': []}
            print("数据库错误|select_all %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def insert_data(self, condition, params):
        try:
            results = self.cur.executemany(condition, params)
            self.conn.commit()
            result = {'code': '0000', 'message': '执行插入操作成功', 'data': results}
        except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': '执行插入操作异常', 'data': []}
            print("数据库错误|insert_data %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()


if __name__ == "__main__":
    test = OperationDbInterface()
    result_select_all = test.select_all("SELECT * FROM config_total")
    result_select_one = test.select_one("SELECT * FROM config_total WHERE id=1")
    result_op_sql = test.op_sql("UPDATE config_total set value_config='test' WHERE id=1")
    result = test.insert_data(""
                              "insert into config_total(key_config,value_config,description,status) values(%s,%s,%s,%s)",
                              [('mytest1', 'mytest11', '我的测试1', 1),
                               ('mytest2', 'mytest22', '我的测试2', 0)])

    print(result_select_all['data'], result_select_all['message'])
    print(result_select_one['data'], result_select_one['message'])
    print(result_op_sql['data'], result['message'])
