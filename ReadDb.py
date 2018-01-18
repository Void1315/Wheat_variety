import pymysql

def get_tuple(tuple_):
    if len(tuple_) == 1 and type(tuple_[0]) == tuple:
        tuple_ = tuple_[0]
    return tuple_


class MyLink:
    """
        读取数据库
    """
    # my_config = {
    #     'host': '123.206.16.158',
    #     'port': 3306,
    #     'user': 'ubuntu',
    #     "password": "wangqihang007",
    #     'db': 'wheat_query',
    # }
    my_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        "password": "wqld1315",
        'db': 'wheat_query',
    }
    link = None  # 我的连接
    field_list = [
        "id",
        "wheat_id",
        "ecology_type",
        "seed_nature",
        "tiler_nature",
        "plant_type",
        "spike_length",
        "leaf_nature",
        "spike_layer",
        "plant_height",
        "lodging",
        "panicle_type",
        "root_activ",
        "yellow",
        "panicle_num",
        "grain_num",
        "ths_weight",
        "resistance",
        "protein",
        "volume",
        "wet_gluten",
        "fall_num",
        "precipitate",
        "water_uptake",
        "format_time",
        "steady_time",
        "weaken",
        "hardness",
        "white",
        "powder",
        "yield_result",
        "tech_point"
    ]   # 字段的所有值
    def __init__(self):
        self.link = pymysql.connect(**self.my_config)

    def check_field(self,field):
        if ',' in field:
            list_ = field.split(',')
            if not set(self.field_list)>set(list_):
                raise Exception("无此字段值", field)
        elif field not in self.field_list:
            raise Exception("无此字段值", field)

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

    def select_field(self,field):
        self.check_field(field)
        the_sql = "SELECT "+field+" FROM wheat_attr"
        with self.link.cursor() as cursor:
            cursor.execute(the_sql)
            result = cursor.fetchall()
            return result
        
    def ill_name_to_id(self,ill_str):
        """
        通过病的名称查询id
        :param ill_str:病的名称
        :return:int的id值
        """
        with self.link.cursor() as cursor:
            the_sql = "SELECT ill.id FROM ill WHERE ill.NAME like %s "
            cursor.execute(the_sql, ("%" + ill_str + "%",))
            return cursor.fetchall()[0][0]
            
    def get_ill_id(self,target, kind,field = "ill"):
        """
        通过传来的病名和特性，比如传来“条锈病”，“感”
        则返回，具有“（高、低、中）感条锈病”的小麦id和，不具有的小麦id
        :param target:病的名称
        :param kind:病的特征（慢、感、抗）
        :return:两个list，一个是具有的id，一个是不具有的id
        """
        with self.link.cursor() as cursor:
            ill_id = self.ill_name_to_id(target)
            the_sql = "SELECT wheat_attr.`wheat_id` FROM wheat_attr WHERE wheat_attr.`wheat_id` NOT IN " \
                      "(SELECT wheat_ill.`wheat_id` FROM wheat_ill WHERE wheat_ill.`ill_id` = %s AND wheat_ill.`kind` LIKE %s)"
            cursor.execute(the_sql, (ill_id, "%" + kind + "%",))
            not_in_list = [val[0] for val in cursor.fetchall()]
            the_sql = "SELECT wheat_ill.`wheat_id` FROM wheat_ill " \
                      "WHERE wheat_ill.`ill_id` = %s AND wheat_ill.`kind` LIKE %s "
            cursor.execute(the_sql, (ill_id, "%" + kind + "%",))
            in_list = [val[0] for val in cursor.fetchall()]
            return in_list,not_in_list

    def get_att_id(self, target,field, kind=""):
        """
        :param target:特征词，如 幼苗匍匐
        :param field:预测字段
        :param kind:没什么用
        :return:两个list，一个是具有的id，一个是不具有的id
        """
        if field not in self.field_list:
            raise Exception("查询字段不在范围",field)
        with self.link.cursor() as cursor:
            the_sql = "SELECT wheat_attr.`wheat_id` FROM wheat_attr WHERE "+field+"  LIKE %s "
            target = "%" + target + "%"
            cursor.execute(the_sql, (target,))
            in_list = [val[0] for val in cursor.fetchall()]
            the_sql = "SELECT wheat_attr.`wheat_id` FROM wheat_attr WHERE "+ field +" NOT LIKE %s "
            cursor.execute(the_sql, (target,))
            not_in_list = [val[0] for val in cursor.fetchall()]
            return in_list,not_in_list

    def get_attr_with_id(self,id):
        with self.link.cursor() as cursor:
            the_sql = ""
        pass
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
