import nltk, pprint

str_ = '''抗病性鉴定，秆锈病免疫，高抗叶锈病，中感赤霉病和根腐病，高感白粉病。'''
list_ill = []


def get_RecentSymbol(str_):
	commo = str_.find('，')
	over = str_.find('。')
	if commo == -1 and over == -1:
		return len(str_)
	if commo == -1:
		return over
	elif over == -1:
		return commo
	else:
		return commo if commo < over else over

list_ = None

def split_with(str_, the_feature):
	global list_ill, list_
	if "和" in str_:
		list_ = str_.split('和')
		for i in range(len(list_)):
			split_with(list_[i], the_feature)
	if "、" in str_:
		list_ = str_.split('、')
		for i in range(len(list_)):
			split_with(list_[i], the_feature)
	if "和" not in str(list_) and "、" not in str(list_):
		list_ill += [the_feature+vel[:5] for vel in list_]
		for index_,val in enumerate(list_ill):
			if val[:len(the_feature)]==val[len(the_feature):len(the_feature)*2]:
				list_ill[index_] = val[len(the_feature):]
	return list(set(list_ill))

def serchModifiers(str_):
	the_code = []
	for index, val in enumerate(str_):
		feature_mod = 0
		if val == "高" or val == "中" or val == "低":
			feature_mod = 2
		elif val == "慢":
			feature_mod = 1
		if feature_mod != 0:
			the_feature = str_[index:index + feature_mod]  # 修饰词
			com_index = get_RecentSymbol(str_[index:])
			if com_index != -1:
				the_illset = str_[index:index + com_index]
				if "和" in the_illset:
					the_code += split_with(str_[index:index + com_index],the_feature)
				elif "、" in the_illset:
					the_code += split_with(str_[index:index + com_index],the_feature)
				else:
					the_code += [str_[index:index + com_index]]
		# else:
		# 	if val=="病":
				# the_code += (str_[index-2:index+1])
	return ','.join(list(set(the_code)))


print(serchModifiers(str_))


classifier = nltk.NaiveBayesClassifier.train([({'病理性': "中感条绣病，高感白粉病，叶锈病，赤霉病，纹枯病",
'抗性':'无'}, '第一种小麦'),({'病理性': "条锈病免疫、高感叶锈病、纹枯病、白粉病和赤霉病。",
'抗性':'抗寒性好'}, '第二种小麦')])
print(classifier.classify({'病理性': "叶锈病，赤霉病，纹枯病",
'抗性':'抗寒性好'}))