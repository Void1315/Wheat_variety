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
        "panicle_num",
        "grain_num",
        "ths_weight",
        "resistance",
        "protein",
        "volume",
        "wet_gluten",
        "fall_num",
        "precipitate",
        "water_uptake",
        "format_time",
        "steady_time",
        "weaken",
        "hardness",
        "white",
        "powder",
        "yield_result",
        "tech_point"
    ]   # 字段的所有值
    file_dir = "field_dict\\"
    def __init__(self):
        from ReadDb import MyLink
        from Resistance import FeatureManager
        
        self.my_sql = MyLink()
        self.FeatureObject = FeatureManager()
        
    def save_date(self,file_name,date):
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
        date = self.FeatureObject.get_set_this_feature(field,str_)
        return date
    
    def update_one(self,field):
        model = self.my_sql.select_field(field)
        date = []
        for val in model:
            date.append(self.get_date(field,val[0]).split(','))
        self.save_date(field,date)
        
    def update_all(self):
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
                
        
if __name__=='__main__':
    the_savefile = SaveFile()
    the_savefile.update_all()
    # the_list = [1,2,3]
    # one_list = [3,4,5]
    # for i in the_list:
    #     if