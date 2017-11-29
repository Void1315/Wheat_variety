import pymysql, pprint
import re
from Resistance import Resistance
from Resistance import FeatureManager

def get_tuple(tuple_):
    if len(tuple_) == 1 and type(tuple_[0]) == tuple:
        tuple_ = tuple_[0]
    return tuple_


class MyLink:
    """
        读取数据库
    """
    my_config = {
        'host': '123.206.16.158',
        'port': 3306,
        'user': 'ubuntu',
        "password": "wangqihang007",
        'db': 'wheat_query',
    }
    link = None  # 我的连接

    def __init__(self):
        self.link = pymysql.connect(**self.my_config)

    def select_resistance(self):
        """
        查询 resistance 字段内容
        :return:一个list，其元素为元祖（id，resistance）,包含所有resistance的值
        """
        the_list = []
        the_sql = "SELECT id,resistance FROM wheat_attr"
        with self.link.cursor() as cursor:
            cursor.execute(the_sql)
            result = cursor.fetchall()
            for val in result:
                if len(val[1]) > 1:
                    the_list.append((val[0], val[1]))
        return the_list

    # def get_cloud_with_id(self, cloud, *arg):
    #     """
    #     根据传递的列名和id值返回结果
    #     返回单列,并在此提取了特征，通过在构造dict时
    #     :param cloud: 接受查询的列
    #     :param arg: 用于接收id元祖，可以传递（19,55,45）形式也可以传递15,54,56
    #     :return:返回一个键值对dict 比如{'grain_num': 41.2, 'panicle_num': 41.2, 'ths_weight': 41.2}
    #     """
    #     arg = get_tuple(arg)
    #     the_list = []
    #     obj_featuremanager = FeatureManager()
    #     the_sql = "SELECT " + cloud + " FROM wheat_attr WHERE id IN " + str(arg)
    #     with self.link.cursor() as cursor:
    #         if len(arg)==0:
    #             return the_list
    #         cursor.execute(the_sql)
    #         result = cursor.fetchall()
    #         for val in result:
    #             the_list.append({v:obj_featuremanager.get_set_this_feature(v,k) for v,k in zip(cloud.split(","),val)})
    #     return the_list


if __name__ == "__main__":
    pass
