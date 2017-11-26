import sys
import setModel
import nltk, pprint, random
from ReadDb import MyLink
from Resistance import SetDictFeature

def get_ill():
    the_list = []
    with open('一个.txt','r',encoding='utf8') as f:
        for line in f.readlines():
            the_list.append(line.replace("\n","")[-3:])
    return list(set(the_list))

if __name__ == "__main__":
    the_obj = setModel.SetModel()
    my_link = MyLink()
    my_sql = "panicle_num,grain_num,ths_weight,protein,wet_gluten,ecology_type,seed_nature,tiler_nature,spike_length"
    str_list = get_ill()
    str_list = ["白粉病"]
    # print(str_list)
    list_ = []
    for val in str_list:
        in_list,not_list = the_obj.get_ill_id(val)
        my_list = my_link.get_cloud_with_id(my_sql, tuple(in_list))#此方法通过 含有特征病的id，去找其他数据
        list_ += [(j, val) for j in my_list]
        my_list = my_link.get_cloud_with_id(my_sql, tuple(not_list))  # 此方法通过 含有特征病的id，去找其他数据
        list_ += [(j, "无"+val) for j in my_list]
    random.shuffle(list_)
    print("一共 "+ str(len(list_)) + " 条数据")
    classifier = nltk.NaiveBayesClassifier.train(list_)#生成分类器
    # print(nltk.classify.accuracy(classifier,list_[:5]))#评估分类器
    setModel.cross_validation(10,list_)
    
    dict_ = {'panicle_num': 47, 'grain_num': 47, 'ths_weight': 48 , 'protein':15.0, 'wet_gluten':30.0
                               ,'ecology_type' : "半冬性，全生育期239天，与对照品种洛旱7号相当。",
                               "seed_nature": "幼苗直立，苗势壮，冬季耐寒性较好",
                               "tiler_nature":"分蘖力强。",
                               "spike_length":"穗下节短"}
    the_feature = SetDictFeature(dict_)
    
    print("\n预测的结果是" + classifier.classify(the_feature.set_model()))