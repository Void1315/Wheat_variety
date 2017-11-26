import nltk, pprint, random
from Resistance import Resistance
from ReadDb import MyLink

def cross_validation(fold,list_):
    """
    此方法用于交叉验证，我们使用朴素贝叶斯
    :param fold: 交叉验证倍数
    :param list_: 一个数据集，带标签
    :return:交叉验证的结果
    """
    random.shuffle(list_)
    the_list = []
    sum_ = 0
    one_fold = int(len(list_)/fold+0.5)
    for i in range(fold):
        if i == fold-1:
            the_list.append(list_[i * one_fold:])
        else:
            the_list.append(list_[i*one_fold:(i+1)*one_fold])
    for val in range(fold):
        a_list = []
        b_list = []
        if val==fold-1:
            for i in the_list[0:val]:
                a_list+=i
            classifier = nltk.NaiveBayesClassifier.train(a_list)  # 生成分类器
        else:
            for i in the_list[0:val]+the_list[val+1:]:
                a_list+=i
            classifier = nltk.NaiveBayesClassifier.train(a_list)  # 生成分类器
        sum_ +=nltk.classify.accuracy(classifier, the_list[val])  # 评估分类器
    print(str(fold)+"倍交叉验证的结果是:\n"+str(sum_/fold))

def get_all_ill(filename = '一个.txt'):
    """
    此方法用于获取所有病的字符串
    :param filename: 获取的文件名
    :return:一个list
    """
    the_list = []
    with open(filename,'r',encoding='utf8') as file_:
        for i in file_.readlines():
            the_list.append(i.replace("\n",""))
    return the_list


class SetModel:
    my_db = MyLink()
    my_feature = Resistance()
    the_list = []
    def __init__(self):
        """
        通过构造函数，我们从数据库读出来这个字段数据，和ID 并把它们
        变成一个list里面很多元祖，来生成特征集
        """
        pass
    def get_list(self):
        """
        只是从resistance这个字段获取数据
        :return: 我们返回特征集list({...},id)
        """
        # pprint.pprint(self.__the_list)
        for id, resistance in self.my_db.select_resistance():
            self.my_feature.str_ = resistance
            the_txt = self.my_feature.get_feature_dict()
            self.the_list.append((the_txt.copy(), int(id)))
        return self.the_list.copy()

    def get_ill_id(self, str_):
        """
        :type str_: str
        :param str_: 抗病性的哪一种特征，比如高抗条纹病，如果
        含条纹病，则含有（抗条纹病和感条纹病的都含在里面）
        :return: 含有关键词的list 里面是id，只是id，所以我们应该用id去查其他数据
        返回的第二个值是不含关键病的list
        """
        the_list = self.get_list()
        list_ = []
        not_list = []
        for val in the_list:
            if str_ in val[0]["抗病性"]:
                list_.append(val[1])
            else:
                not_list.append(val[1])
        return list_,not_list.copy()
        

if __name__ == "__main__":
    the_obj = SetModel()
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
    cross_validation(10,list_)
    print(classifier.classify({'panicle_num': 47, 'grain_num': 47, 'ths_weight': 48 , 'protein':15.0, 'wet_gluten':30.0
                               ,'ecology_type' : "半冬性，全生育期239天，与对照品种洛旱7号相当。",
                               "seed_nature": "幼苗直立，苗势壮，冬季耐寒性较好",
                               "tiler_nature":"分蘖力强。",
                               "spike_length":"穗下节短"}))
    # print(classifier.show_most_informative_features(5))#检查似然比