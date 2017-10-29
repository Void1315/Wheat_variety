# coding=utf-8
import re, jieba

jieba.load_userdict("dict/dict_1.txt")


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
            return ','.join(the_code)
        else:
            return "无"

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
            the_reul = "[，|。]+.*.病免疫"
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
            "免疫性": '无',
            "抗旱性": "无",
            "抗寒性": "无"
            }
        :return:一个字典
        """

        self.the_feature_dict["抗病性"] = (self.get_ill())
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
        return list_.copy()


class Seed_nature:
    str_ = ""

    def __init__(self, str_=""):
        self.str_ = str_

    def get_seed_feature(self):
        seg_list = jieba.cut(self.str_, cut_all=True)
        print("Full Mode: " + "/ ".join(seg_list))  # 全模式


if __name__ == "__main__":
    # the_obj = Resistance('''抗病性鉴定，秆锈病免疫，中感叶锈病和根腐病，高感赤霉病和白粉病。''')  #
    # print(the_obj.get_feature_dict())

    # print(the_obj.the_feature_dict)


    # the_obj_E = Ecology_type("属弱春性多穗型早熟品种，平均全生育期229.3天")
    # print(the_obj_E.get_ecology_feature())

    the_obj = Seed_nature("幼苗直立，苗势壮，叶短宽、浓绿色，耐寒性较好")
    the_obj.get_seed_feature()
