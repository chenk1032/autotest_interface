# -*- coding:utf-8 -*-
# __author__ = 'cxx copy from ...'
"""
Config
"""
import os

# 当前代码所在目录的上级目录
src_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 导出的excel表格标题
field_excel = ['编号', '接口名称', '用例级别',
               '请求类型', '接口地址', '接口头文件', '接口请求参数',
               '接口返回包', '待比较参数', '实际参数值', '预期参数值', '参数值比较结果',
               '待比较参数集合', '实际参数集合', '参数完整性结果',
               '用例状态', '创建时间', '更新时间']
db_connection = {'host_db': '127.0.0.1', 'user_db': 'test_user1', 'passwd_db': 'test_user1',
                 'name_db': 'test_interface',
                 'port_db': 3306, 'link_type': 0}
