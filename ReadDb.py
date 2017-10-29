import pymysql, pprint
import re


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

	def get_cloud_with_id(self, cloud, *arg):
		"""
		根据传递的列名和id值返回结果
		返回单列
		:param cloud: 接受查询的列
		:param arg: 用于接收id元祖，可以传递（19,55,45）形式也可以传递15,54,56
		:return:返回一个键值对dict 比如{'grain_num': 41.2, 'panicle_num': 41.2, 'ths_weight': 41.2}
		"""
		arg = get_tuple(arg)
		the_list = []
		the_sql = "SELECT " + cloud + " FROM wheat_attr WHERE id IN " + str(arg)
		with self.link.cursor() as cursor:
			if len(arg)==0:
				return the_list;
			cursor.execute(the_sql)
			result = cursor.fetchall()
			for val in result:
				the_list.append({v:k for v in cloud.split(",") for k in val})
		return the_list


if __name__ == "__main__":
	the_obj = MyLink()
	pprint.pprint(the_obj.get_cloud_with_id("weaken,powder", (23, 77)))

# pattern = re.compile('[抗旱级别]+\d+[级]')
# pattern = re.compile(r'抗旱+.+([0-9]级|[高|中|低]+等)')
# str = '中感白粉病和纹枯病，高感条锈病，中抗叶锈病和叶枯病。2008年、2009两年度经洛阳农科院全生育期抗旱鉴定：3级，抗旱性中等'
# print(pattern.search(str).)
