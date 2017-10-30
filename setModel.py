import nltk, pprint, random
from Resistance import Resistance
from ReadDb import MyLink


class SetModel:
	my_db = MyLink()
	my_feature = Resistance()
	the_list = []

	def __init__(self):
		"""
		通过构造函数，我们从数据库读出来这个字段数据，和ID 并把它们
		变成一个list里面很多元祖，来生成特征集
		"""
	def get_list(self):
		"""
		:return: 我们返回特征集
		"""
		# pprint.pprint(self.__the_list)
		for i, j in self.my_db.select_resistance():
			self.my_feature.str_ = j
			the_txt = self.my_feature.get_feature_dict()
			self.the_list.append((the_txt.copy(), int(i)))

		return self.the_list.copy()

	def get_ill_id(self, str_):
		"""
		:type str_: str
		:param str_: 抗病性的哪一种特征，比如高抗条纹病，如果
		传条纹病，则含有（抗条纹病和感条纹病的都含在里面）
		:return: 含有关键词的list 里面是id
		"""
		the_list = self.get_list()
		list_ = []
		for val in the_list:
			if str_ in val[0]["抗病性"]:
				list_.append(val[1])
		return list_


if __name__ == "__main__":
	the_obj = SetModel()
	my_link = MyLink()
	my_sql = "panicle_num,grain_num,ths_weight,protein,wet_gluten"
	str_list = ["高感叶锈病","中感白粉病"]
	list_ = []
	for val in str_list:
		my_list = my_link.get_cloud_with_id(my_sql, tuple(the_obj.get_ill_id(val)))
		list_ += [(j, val) for j in my_list]

	random.shuffle(list_)
	pprint.pprint(list_[:5])
	classifier = nltk.NaiveBayesClassifier.train(list_[5:])#生成分类器
	print(nltk.classify.accuracy(classifier,list_[:5]))#评估分类器
	# print(classifier.classify({'panicle_num': 47, 'grain_num': 47, 'ths_weight': 48}))
	print(classifier.show_most_informative_features(5))#检查似然比