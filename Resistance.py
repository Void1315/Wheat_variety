# coding=utf-8
import re, jieba
import jieba.posseg as pseg

jieba.load_userdict("dict/dict_1.txt")


"""
此文件是用来提取特征的,如果像float、int类型的字段就没有提特征的必要
所以文件是主要为varchar类型字段服务，
现在能提取特征的字段有：
其中类文件有：
Ecology_type
Seed_nature
Resistance这个比较特殊，抗病性和免疫性还有抗寒抗旱性
这些是方法：
seed_nature,tiler_nature,plant_type,spike_length
leaf_nature,spike_layer,plant_height,lodging,panicle_type
root_activ,yellow
"""


def is_number(s):
    """
    :param s:传递一个字符串
    :return: 如果为数字，返回True，否则返回False
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def get_RecentSymbol(str_):
    """
    判断距离那个符号近
    :param str_:
    :return:
    """

    comma = str_.find('，')
    over = str_.find('。')
    if comma == -1 and over == -1:
        return len(str_)
    if comma == -1:
        return over
    elif over == -1:
        return comma
    else:
        return comma if comma < over else over


def split_ill(str_, the_feature):
    """
    :param str_: 一个字符串
    :param the_feature:特征关键字
    :return:一个list，里面存储这个病
    """
    the_str_ = str_.replace('、', "，" + the_feature)
    return the_str_.replace("和", "，" + the_feature)

class Resistance:
    the_feature_dict = {
        "抗病性": "无",
        "感病性": "无",
        "免疫性": '无',
        "抗旱性": "无",
        "抗寒性": "无"
    }  # 构造完成的字典
    str_ = ""  # 描述字符串
    list_ = None
    list_ill = []

    def __init__(self, str_="无"):
        self.str_ = str_

    def split_with(self, str_, the_feature):
        """
        用‘和’或者‘、’来区分连词，
        高感叶锈病、纹枯病、白粉病和赤霉病
        :param str_:带修饰词的一串字符穿
        :param the_feature:特征词也就是修饰词，比如高感
        :return:返回一个加上修饰词的病理性【高感叶锈病，高感纹枯病...】
        """
        if "和" in str_:
            self.list_ = str_.split('和')
            for i in range(len(self.list_)):
                self.split_with(self.list_[i], the_feature)
        if "、" in str_:
            self.list_ = str_.split('、')
            for i in range(len(self.list_)):
                self.split_with(self.list_[i], the_feature)
        if "和" not in str(self.list_) and "、" not in str(self.list_):
            self.list_ill += [the_feature + vel[:5] for vel in self.list_]
            for index_, val in enumerate(self.list_ill):
                if val[:len(the_feature)] == val[len(the_feature):len(the_feature) * 2]:
                    self.list_ill[index_] = val[len(the_feature):]
        return list(set(self.list_ill))

    def get_ill(self):
        """
        :return:返回病理性字符串，用‘，’号分割
        """
        the_code = []
        for index, val in enumerate(self.str_):
            feature_mod = 0
            if (val == "高" or val == "中" or val == "低") and self.str_[index + 1] != "等":
                feature_mod = 2
            elif val == "慢":
                feature_mod = 1
            if feature_mod != 0:
                the_feature = self.str_[index:index + feature_mod]  # 修饰词
                com_index = get_RecentSymbol(self.str_[index:])
                if com_index != -1:
                    the_illset = self.str_[index:index + com_index]
                    if "和" in the_illset or "、" in the_illset:
                        the_code.append(split_ill(self.str_[index:index + com_index], the_feature))
                    else:
                        the_code.append(the_illset)
        if len(the_code) > 0:
            the_list = '，'.join(the_code).split("，")
            for index,val in enumerate(the_list):
                if '病' not in val:
                    the_list[index] = the_list[index]+"病"
            return ','.join(the_list)
        else:
            return "无"

    def get_disill(self,list_):
        the_list = []
        for val in list_:
            if "抗" in val:
                the_list.append(val)
        return the_list
    
    def get_illlist(self,list_):
        the_list = []
        for val in list_:
            if "抗" not in val :
                the_list.append(val)
        return the_list
    
    
    def get_immune(self):
        """
        获得免疫特征，
        :return: 返回字符串
        """
        list_ = []
        the_model = True
        if self.str_.find("免疫") > 0:
            index_ill = self.str_.index("免疫")
        else:
            return "无"
        if self.str_[index_ill - 1:index_ill] == "病":
            the_reul = "[，|。]+.？*.病免疫"
            the_model = False
        else:
            the_reul = "免疫*?.*?病[、|和]*?.*?[。|，]"

        result = re.search(the_reul, self.str_)
        if result is not None:
            the_str = self.str_[result.start():result.end()]
            if "和" in the_str or "、" in the_str or "，" in the_str:
                self.list_ = ""
                self.list_ill = []
                if "。" in the_str:
                    the_str = the_str.replace("。", "")
                if "，" in the_str:
                    the_str = the_str.replace("，", "")
                if not the_model:
                    return ",".join(the_str.split("免疫"))[:-1]
                else:
                    the_list = self.split_with(the_str, "免疫")
                    for val in the_list:
                        list_.append(val[2:])
                    return ",".join(list_)
            else:
                return the_str[2:-1]
        else:
            return "无"

    def get_natural(self, the_mode):
        """
        获得环境数据，比如抗旱性，
        :param the_mode:提取模式
        :return:字符串比如：“一级，中”
        """
        the_str = "抗" + the_mode + "+.+([0-9]级|[高|中|低]+等)"
        the_lv = "[0-9]"  # 找等级
        the_chlv = "[高|中|低]"  # 找汉字等级
        the_rule = re.search(the_str, self.str_)
        if the_rule is not None:
            my_str = self.str_[the_rule.start():the_rule.end()]

            the_lv_result = my_str[re.search(the_lv, my_str).start():re.search(the_lv, my_str).end()] \
                if re.search(the_lv, my_str) is not None else "无"

            the_chlv_result = my_str[re.search(the_chlv, my_str).start():re.search(the_chlv, my_str).end()] \
                if re.search(the_chlv, my_str) is not None else "无"

            return the_lv_result + '，' + the_chlv_result
        else:
            return "无"

    def get_feature_dict(self):
        """
        返回抗病性字段所拆分出来的特征集，
        由键值对给出
            the_feature_dict = {
            "抗病性": "无",
            "感病性": "无",
            "免疫性": '无',
            "抗旱性": "无",
            "抗寒性": "无"
            }
        :return:一个字典
        """
        ill_list = self.get_ill().split(',')
        
        self.the_feature_dict["抗病性"] = ','.join(self.get_disill(ill_list))
        self.the_feature_dict["感病性"] = ','.join(self.get_illlist(ill_list))
        self.list_ill = []
        self.the_feature_dict["免疫性"] = (self.get_immune())
        self.the_feature_dict["抗旱性"] = (self.get_natural("旱"))
        self.the_feature_dict["抗寒性"] = (self.get_natural("寒"))
        return self.the_feature_dict.copy()


class Ecology_type:
    '''
        此类表示对ecology字段的分词，
    '''
    str_ = ''

    def __init__(self, str_):
        self.str_ = str_

    def get_ecology_feature(self):
        """
        返回 这个字符串含有的特征
        :return: 一个字符串存放特征
        """

        seg_list = jieba.cut(self.str_, cut_all=False)
        # print("Full Mode: " + "/ ".join(seg_list))  # 全模式
        the_list = [i for i in seg_list]
        list_ = []
        for index, val in enumerate(the_list):
            if val.find("性") > 0:
                list_.append(val)
            if val.find("育期") > 0 and is_number(the_list[index + 1]):
                list_.append(the_list[index + 1])
            if val.find("型") > 0:
                list_.append(val)
        if len(the_list) == 0:return [""]
        return list_.copy()

class FeatureManager:
    flag_list = {   #需要的词性，和不需要的词性，元祖第一个是需要的,空表示没有
        "seed_nature":(['v','a'],[]),
        "tiler_nature":(['b','a'],[]),
        "plant_type":(['a'],[]),
        "spike_length":([],[]),
        "leaf_nature":(['a','v','b'],[]),
        "spike_layer":([],[]),
        "plant_height":(['m','x','eng'],[]),
        "lodging":([],['x']),
        "panicle_type":([],['x']),
        "root_activ": ([],['x']),
        "yellow":([],['x']),
        "yield_result":([],['n','x']),
        "tech_point":([],['x'])
        
    }
    str_ = ""   #提取特征的句子
    field= ""   #特征名字
    the_list = []   #提取特征后的list
    def __init__(self,field="",str_=""):
        """
        可以通过构造函数，把提取特征的标签，和标签值初始化了
        :param field: 标签
        :param str_: 值
        """
        self.str_ = str_
        self.field = field
        
    def set_field_str(self,field,str_):
        """
        如果你错过了构造函数，没关系我们有set方法，
        可以让你重新对标签和值进行设置
        :param field:标签
        :param str_:值
        :return:没有返回值
        """
        self.field = field
        self.str_ = str_
    
    def get_this_feature(self):
        """
        
        :return: 通过预先设定好的标签和值，我们来提取这句话对应的特征，
        返回一个string
        """
        b_is, val = self.special_features()
        if b_is:
            return val
        if self.not_str_feature():
            return self.str_
        return ','.join(self.split_words())
        
    def get_set_this_feature(self,field,str_):
        """
        如果你在循环中，不想通过构造和，set方法，我们也有办法
        通过直接设置值，来获得特征语句
        :param field: 标签
        :param str_: 值
        :return: 特征字符串
        """
        self.field = field
        self.str_ = str_
        if str_ is None:
            self.str_ = ""
        return self.get_this_feature()
    
    def split_words(self):
        """
        
        :return: 分词逻辑，我们会用flag_list里面的分词规则，对特征进行提取
        要知道，如果没有提取词的词性，那么我们会全部提取，
        如果没有非提取词的词性，那么我们不会舍弃
        """
        self.the_list = []
        if self.str_ is None or len(self.str_)==0:
            return [""]
        words = pseg.cut(self.str_)
        for word, flag in words:
            if flag  in self.flag_list[self.field][1]:
                continue
            if len(self.flag_list[self.field][0])==0:#全模式
                self.the_list.append(word)
            else:
                if flag in self.flag_list[self.field][0]:
                    self.the_list.append(word)
        return self.the_list
    
    def not_str_feature(self):
        """
        判断你给我的特征，是否有预设值，如果没有则返回False
        :return:一个bool值
        """
        if self.field not in self.flag_list:
            return True
        else:
            return False
    
    def special_features(self):
        """
        一些特殊的分词方式，比如复杂的分词如抗病性，
        
        :return: 返回值是两个，一个是True必须，另一个是特征字符串
        """
        if self.field == "ecology_type":
            the_obj = Ecology_type(self.str_)
            return True,','.join(the_obj.get_ecology_feature())
        elif self.field == 'resistance':
            the_obj = Resistance(self.str_)
            return True,(the_obj.get_feature_dict()["抗病性"])
        else:
            return False,""

class SetDictFeature(FeatureManager):
    """
    此类是继承了FeatureManager，是为了更方便的提取特征，
    我们用这个类是为了直接从dict中提取特征，
    一般适用于用户直接给我预测数据，然后我们稍加处理
    """
    dict_ = {}
    def __init__(self,dict_ = None):
        """
        :param dict_: 必须传入一个dict类型
        """
        self.dict_ = dict_
    def set_model(self,dict_ = None):
        """
        通过父类提取特征
        :return: 一个dict，不过是全部提取好特征的
        """
        if dict_ is None and self.dict_ is None:
            return
        if dict_ is None and self.dict_  is not None:
            dict_ = self.dict_.copy()
        the_dict = {}
        for index in dict_:
            the_dict[index] = self.get_set_this_feature(index,dict_[index])
        return the_dict
    
if __name__ == "__main__":
    the_dict = {'panicle_num': 47, 'grain_num': 47, 'ths_weight': 48 , 'protein':15.0, 'wet_gluten':30.0
                               ,'ecology_type' : "半冬性，全生育期239天，与对照品种洛旱7号相当。",
                               "seed_nature": "幼苗直立，苗势壮，冬季耐寒性较好",
                               "tiler_nature":"分蘖力强。",
                               "spike_length":"穗下节短"}
    
    
    the_obj = Resistance('''幼苗半直立，分蘖力较强，叶色浅绿，生长势较旺。''')  #
    import  pprint
    pprint.pprint(the_obj.get_feature_dict())

    # the_obj = SetDictFeature(the_dict)
    # the_obj.set_model()

    # print(the_obj.the_feature_dict)

    # the_obj_E = Ecology_type("属弱春性多穗型早熟品种，平均全生育期229.3天")
    # print(the_obj_E.get_ecology_feature())


    # print(get_seed_nature_feature("幼苗半直立，叶色青绿，长势偏旺，冬季抗寒能力差"))

    # print(get_tiler_nature_feature("分蘖力较弱，成穗率较高，成穗数中等。春季起身较早，两极分化较快，抽穗早。"))

    # print(get_spike_length_feature("穗下节长"))

    # print(get_leaf_nature_feature("成株期旗叶及下部叶片较大"))
    
    # print(get_plant_height_feature("株高78+80cm"))
    
    # print(get_lodging_feature("茎秆蜡质厚,茎秆弹性一般,抗倒能力中等"))
    
    # print(get_panicle_type_feature("纺锤形大穗,短芒,白壳,白粒,大小较匀,半角质,饱满度较好,黑胚率高"))
    
    # print(get_root_activ_feature("根系活力强，后期叶功能好，耐高温"))
    
    str_ = """
    幼苗半直立，分蘖力较强，叶色浅绿，生长势较旺。
    """

    the_obj = FeatureManager('seed_nature',str_)
    print(the_obj.get_this_feature())
    words = pseg.cut(str_.strip())
    for word, flag in words:
        print('%s %s' % (word, flag))
    pass