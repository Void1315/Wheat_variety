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

def set_target(target, method, field="ill", kind="", right_kind="", not_kind="", db_link=MyLink(),
               the_model=SetDictFeature()):
    """
    :param setmodel_obj:
    :param target:目标分类依据,如 幼苗半匍匐，
    :param method:动态方法名
    :param kind:分类的字符串
    :param field:
    :param right_kind:正确的分类字符串前缀
    :param not_kind:错误的 同上
    :param db_link:ReadDb对象
    :param the_model:SetDictFeature 对象
    :return:一个list,其中已经分好类了
    """
    method = getattr(db_link,method)#动态调用方法
    list_ = []
    in_list, not_list = method(target,field,kind)  # 这点可以改正为动态调用方法
    for id in in_list:
        list_ += [(the_model.set_model(db_link.get_cloud_with_id(id)),right_kind + kind + target)]
    for id in not_list:
        list_ += [(the_model.set_model(db_link.get_cloud_with_id(id)), not_kind + kind + target)]
    random.shuffle(list_)
    return list_

def feature_one(target,field = "ill" , kind = ""):
    """
    传递一个预测病例，如 条锈病
    :param target:分类依据 如幼苗匍匐
    :param field:预测的字段
    :param kind:针对于病来说的，其他字段不要传值
    :return:一个预测模型
    """
    the_model = SetDictFeature()
    my_link = MyLink()
    if field is "ill":method = "get_ill_id"
    else:method = "get_att_id"
    list_ = set_target(target=target,method=method,kind=kind,not_kind="非",
                       db_link=my_link,the_model=the_model,field = field)
    classifier = nltk.NaiveBayesClassifier.train(list_)#生成分类器
    setModel.cross_validation(10,list_)
    dict_ = {'panicle_num': 43, 'grain_num': 30, 'ths_weight':42 , 'protein':15, 'wet_gluten':32
                               ,'ecology_type' : "属弱春性中熟强筋品种，全生育期220天。",
                               # "seed_nature": "幼苗匍匐，苗势壮，叶片窄卷曲，叶色浓绿，冬季抗寒性较好。",
                               "tiler_nature":"东前分蘖力较弱，分蘖成穗率一般，春季起身拔节较迟，两极分化快，耐倒春寒能力中等。",
                               "spike_length":"",
                                "resistance":"高抗条绣病，高感叶锈病、白粉病、赤霉病、纹枯病。"}
    # dict_ = {'panicle_num': 43, 'grain_num': 30, 'ths_weight':42 , 'protein':15, 'wet_gluten':32
    #                            ,'ecology_type' : "属弱春性中熟强筋品种，全生育期220天。",
    #                            # "seed_nature": "幼苗直立，苗势壮，叶片短直立，冬季抗寒性较好。",
    #                            "tiler_nature":"分蘖力强。",
    #                            "spike_length":"穗下节短"}
    the_feature = the_model.set_model(dict_)
    # print(the_feature)
    print("\n预测的结果是" + classifier.classify(the_feature))

if __name__ == "__main__":
    # feature_one("白粉病","感",field = "ill")
    feature_one("幼苗匍匐", field="seed_nature")

    
    
    # the_sql = "SELECT DISTINCT wheat_attr.`wheat_id` AS attr,wheat_ill.`wheat_id` " \
    #           "AS ill FROM wheat_attr RIGHT JOIN wheat_ill ON wheat_attr.`id` = wheat_ill.`wheat_id`"
    # with my_link.link.cursor() as cursor:
    #     cursor.execute(the_sql)
    #     result = cursor.fetchall()
    #     the_sql = "UPDATE wheat_ill SET wheat_ill.`wheat_id` = %s WHERE wheat_ill.`wheat_id` = %s;"
    #     for date in result:
    #         cursor.execute(the_sql,(date[0],date[1]))
    #         my_link.link.commit()

    # from Resistance import Resistance
    # setmodel_obj = setModel.SetModel()
    # the_model = SetDictFeature()
    # my_link = MyLink()
    # the_obj = Resistance()
    # the_list = my_link.select_resistance()
    # for val in the_list:
    #     gan_list = []
    #     kang_list = []
    #     wheat_id = val[0]
    #     the_obj.str_ = val[1]
    #     feaut_list = the_obj.get_feature_dict()
    #
    #     for the_val in feaut_list["免疫性"].split(','):
    #         # print(the_val)
    #         if len(feaut_list["免疫性"])>1:
    #             kang_list.append(feaut_list["免疫性"])#做到了第三步，该插数据了
    #     for kang_val in kang_list:
    #         the_sql = "SELECT ill.id FROM ill WHERE ill.`name` LIKE %s"
    #         with my_link.link.cursor() as cursor:
    #             print(kang_val)
    #             cursor.execute(the_sql,(kang_val,))
    #             result = cursor.fetchall()
    #             for kang_ill_id in result:
    #                 the_sql = "INSERT INTO wheat_ill (wheat_id,ill_id,kind) VALUES (%s,%s,%s)"
    #                 cursor.execute(the_sql, (int(wheat_id),int(kang_ill_id[0]),'免疫'))
    #                 my_link.link.commit()
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