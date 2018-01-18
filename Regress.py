from sklearn import linear_model
class SaveFile:
    """
    此类是用于从数据库，拿出某字段的所有值，然后分词，存入文件，生成字典的
    """
    
    field_list = [
        "ecology_type",
        "seed_nature",
        "tiler_nature",
        "plant_type",
        "spike_length",
        "leaf_nature",
        "spike_layer",
        "plant_height",
        "lodging",
        "panicle_type",
        "root_activ",
        "yellow",
        "resistance",
        "yield_result",
        "tech_point"
    ]   # 字段的所有值
    file_dir = "field_dict\\"
    def __init__(self):
        """
        生成两个对象，一个是MyLink，另一个是FeatureManager(特征提取器对象)
        """
        from ReadDb import MyLink
        from Resistance import FeatureManager
        
        self.my_sql = MyLink()
        self.FeatureObject = FeatureManager()
        
    def save_date(self,file_name,date):
        """
        通过字段名字和date数据来更新，保存字典
        :param file_name:字段名字
        :param date:数据应为此字段的值得list
        :return:无
        """
        with open(self.file_dir + file_name +'.txt','a+',encoding = 'utf8') as f:
            lines = f.readlines()
            the_list = lines.copy()
            for date_val in date:
                if date_val is not list:
                    date_val = str(date_val)
                    if ',' in date_val:
                        date_val = date_val.split(',')
                    else:
                        date_val = [date_val, ]
                for date_val_val in date_val:
                    if date_val_val not in the_list and len(date_val_val)>0:
                        f.write(date_val_val+'\n')
                        the_list.append(date_val_val)
    
    def get_date(self,field,str_):
        """
        获取提取特征后的值
        :param field:字段名
        :param str_:数据
        :return:一个字符串
        """
        date = self.FeatureObject.get_set_this_feature(field,str_)
        return date
    
    def update_one(self,field):
        """
        此方法用于更新某个字段字典
        :param field: 字段名字
        :return:无
        """
        model = self.my_sql.select_field(field)
        date = []
        for val in model:
            date.append(self.get_date(field,val[0]).split(','))
        self.save_date(field,date)
        
    def update_all(self):
        """
        此方法用于更新所有字典
        :return:无
        """
        import pprint
        import numpy as np
        model = [list(val) for val in self.my_sql.select_field(','.join(self.field_list))]
        date = [self.field_list.copy(),]
        date+=model
        model = np.array(date)
        for index in range(len(self.field_list)):
            for deep,cloud in enumerate(model[:,index]):
                if deep == 0:
                    field = cloud
                    continue
                the_f = self.get_date(field, model[deep][index])
                date[deep][index] = the_f.split(',') if the_f is str else the_f
        date = np.array(date[1:])
        for index in range(len(self.field_list)):
            print(list(date[1:, index]))
            self.save_date(self.field_list[index], list(date[1:, index]))
            

class WordFeature:
    def __init__(self):
        pass

class SetRegressDate:
    the_list = [
        "panicle_num",
        "grain_num",
        "ths_weight",
        "protein"
    ]
    db_link = None
    reg = None#回归对象
    X = None
    y = None
    def __init__(self):
        from ReadDb import MyLink
        self.db_link = MyLink()
        pass
    
    def get_date(self,field):
        if field not in self.the_list:
            raise Exception("无回归提取值", field)
        print(self.db_link.select_field(field))
        
    def set_model(self,filed_list):
        import numpy as np
        model_list = []
        if type(filed_list) is not  list:
            filed_list = [filed_list]
        for index,filed in enumerate(filed_list):
            model_list.append([val[0] for val in self.db_link.select_field(filed)])
        if len(filed_list) == 1:
            return model_list[0]
        list_ = np.array(model_list)
        model_list = []
        for line in range(len(list_[0])):
            model_list.append(list(list_[:,line]))
        return model_list
    
    def set_X(self,reg_list):
        if set(reg_list) < set(self.the_list):
            self.X = self.set_model(reg_list)
        else:
            raise Exception("回归目标不在选择中", reg_list)
        return self
    
    def set_y(self,reg_filed):
        if reg_filed not in self.the_list:
            raise Exception("回归目标不在选择中", reg_filed)
        else:
            self.y = self.set_model(reg_filed)
        return self
    
    def set_reg(self, reg):
        self.reg = reg
        return self
    
    def get_reg(self):
        return self.reg
    
    def fit(self,X = None,y = None):
        if X is None:
            if self.X is None:
                raise Exception("没有X值")
            X = self.X
            y = self.y
        self.reg.fit(X,y)
        return self
    
    def predict(self,X):
        return self.reg.predict(X)
    
    def get_accuracy(self,test_size = 0.25,random_state = 5):
        import sklearn.metrics as sm
        from sklearn import model_selection
        X_train, X_text, y_train, y_test = model_selection.train_test_split(self.X, self.y, test_size=test_size,
                                                                             random_state=random_state)
        y_test_pred = self.reg.predict(X_text)
        print("平均绝对误差 =", round(sm.mean_absolute_error(y_test, y_test_pred), 2))
        print ("均方误差 =", round(sm.mean_squared_error(y_test, y_test_pred), 2))
        print ("中位数绝对误差 =", round(sm.median_absolute_error(y_test, y_test_pred), 2))
        print ("解释方差分数 =", round(sm.explained_variance_score(y_test, y_test_pred), 2))
        print ("R2 score =", round(sm.r2_score(y_test, y_test_pred), 2))
        pass
    
    
    
if __name__=='__main__':
    import numpy as np
    the_date = SetRegressDate()
    reg = linear_model.BayesianRidge()
    the_date.set_X(the_date.the_list[:-1]).set_y(the_date.the_list[-1]).set_reg(reg).fit()
    print(the_date.predict([[38.7,36.7,39.2]]))
    the_date.get_accuracy()
    
    
    
    
    
    
    
    
    # plot_classifer(reg,X,Y)

    # from sklearn import linear_model
    #
    # X = [['a', 0.], ['a', 1.], ['a', 2.], ['a', 3.]]
    # Y = [0., 1., 2., 3.]
    # reg = linear_model.BayesianRidge()
    # reg.fit(X, Y)
    # print(reg.predict([['a',1]]))
    pass
