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

def feature_one(str_):
    """
    传递一个预测病例，如 条锈病
    :param str_:病例字符串
    :return:一个预测模型
    """
    setmodel_obj = setModel.SetModel()
    the_model = SetDictFeature()
    my_link = MyLink()
    list_ = []
    in_list,not_list = setmodel_obj.get_ill_id(str_)
    for id in in_list:
        list_ += [(the_model.set_model(setmodel_obj.get_cloud_with_id(my_link.link,id)),str_)]
    for id in not_list:
        list_ += [(the_model.set_model(setmodel_obj.get_cloud_with_id(my_link.link, id)), "非" + str_)]
    random.shuffle(list_)
    print("一共 "+ str(len(list_)) + " 条数据")#总共就72条数据
    classifier = nltk.NaiveBayesClassifier.train(list_)#生成分类器
    setModel.cross_validation(10,list_)

    dict_ = {'panicle_num': 47, 'grain_num': 47, 'ths_weight': 48 , 'protein':15.0, 'wet_gluten':30.0
                               ,'ecology_type' : "半冬性，全生育期239天，与对照品种洛旱7号相当。",
                               "seed_nature": "幼苗直立，苗势壮，冬季耐寒性较好",
                               "tiler_nature":"分蘖力强。",
                               "spike_length":"穗下节短"}
    the_feature = the_model.set_model(dict_)

    print("\n预测的结果是" + classifier.classify(the_feature))

if __name__ == "__main__":
    feature_one("白粉病")

    
    
    # the_sql = "SELECT DISTINCT wheat_attr.`wheat_id` AS attr,wheat_ill.`wheat_id` " \
    #           "AS ill FROM wheat_attr RIGHT JOIN wheat_ill ON wheat_attr.`id` = wheat_ill.`wheat_id`"
    # with my_link.link.cursor() as cursor:
    #     cursor.execute(the_sql)
    #     result = cursor.fetchall()
    #     the_sql = "UPDATE wheat_ill SET wheat_ill.`wheat_id` = %s WHERE wheat_ill.`wheat_id` = %s;"
    #     for date in result:
    #         cursor.execute(the_sql,(date[0],date[1]))
    #         my_link.link.commit()
        
    
    
    # for val in the_list:
        # gan_list = []
        # kang_list = []
        # wheat_id = val[0]
        # the_obj.str_ = val[1]
        # feaut_list = the_obj.get_feature_dict()
        # for the_val in feaut_list["感病性"].split(','):
        #     if "感" in the_val:
        #         gan_list.append((the_val[2:],the_val[:2]))
        #     if "慢" in the_val:
        #         gan_list.append((the_val[1:],the_val[:1]))
        # for the_val in feaut_list["抗病性"].split(','):
        #     kang_list.append((the_val[2:],the_val[:2]))#做到了第三步，该插数据了
        # for kang_val in kang_list:
        #     the_sql = "SELECT ill.id FROM ill WHERE ill.`name` LIKE %s"
        #     with my_link.link.cursor() as cursor:
        #         cursor.execute(the_sql,(kang_val[0]))
        #         result = cursor.fetchall()
        #         for kang_ill_id in result:
        #             the_sql = "INSERT INTO wheat_ill (wheat_id,ill_id,kind) VALUES (%s,%s,%s)"
        #             cursor.execute(the_sql, (int(wheat_id),int(kang_ill_id[0]),kang_val[1]))
        #             my_link.link.commit()
        # for gan_val in gan_list:
        #     the_sql = "SELECT ill.id FROM ill WHERE ill.`name` LIKE %s"
        #     with my_link.link.cursor() as cursor:
        #         cursor.execute(the_sql, (gan_val[0]))
        #         result = cursor.fetchall()
        #         for kang_ill_id in result:
        #             the_sql = "INSERT INTO wheat_ill (wheat_id,ill_id,kind) VALUES (%s,%s,%s)"
        #             cursor.execute(the_sql, (int(wheat_id), int(kang_ill_id[0]), gan_val[1]))
        #             my_link.link.commit()










    pass