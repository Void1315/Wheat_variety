import sys
import setModel
import nltk, pprint, random
from ReadDb import MyLink
if __name__ == "__main__":
	the_obj = setModel.SetModel()
	my_link = MyLink()
	my_sql = "panicle_num,grain_num,ths_weight,protein,wet_gluten,ecology_type,seed_nature,tiler_nature,spike_length"
	str_list = ["感叶锈病","感白粉病","感条锈病"]
	list_ = []
	for val in str_list:
		my_list = my_link.get_cloud_with_id(my_sql, tuple(the_obj.get_ill_id(val)))
		list_ += [(j, val) for j in my_list]
	random.shuffle(list_)
	# pprint.pprint(list_[:5])
	classifier = nltk.NaiveBayesClassifier.train(list_)#生成分类器
	# print(nltk.classify.accuracy(classifier,list_[:5]))#评估分类器
	setModel.cross_validation(10,list_)
	print(classifier.classify({'panicle_num': 47, 'grain_num': 47, 'ths_weight': 48 , 'protein':15.0, 'wet_gluten':30.0
							   ,'ecology_type' : "半冬性，全生育期239天，与对照品种洛旱7号相当。",
							   "seed_nature": "幼苗直立，苗势壮，冬季耐寒性较好",
							   "tiler_nature":"分蘖力强。",
							   "spike_length":"穗下节短"}))