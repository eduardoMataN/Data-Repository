from apps.dataset import *
class dataBag:
    def __init__(self, dataframes:list[dataset]):
        self.dataframes=self.makeDictionary(dataframes)
        self.default=dataframes[0]
        self.current=dataframes[0]
    def makeDictionary(self, dataframes):
        dictionary={}
        for dataframe in dataframes:
            dictionary[dataframe.title]=dataframe
        return dictionary
    def getDataframe(self,title=None):
        if(title not in self.dataframes.keys() or title==None):
            return self.default
        if(len(self.dataframes)==1):
            return self.default
        return self.dataframes[title]
    def getTitle(self,dataframe):
        for key in self.dataframes:
            if self.dataframes[key]==dataframe:
                return key
    def getByName(self, name:str)->dataset:
        for key in self.dataframes:
            if self.dataframes[key].name==name:
                return self.dataframes[key]
        return None
    def modify_by_name(self, name:str, mode:str):
        for key in self.dataframes:
            if self.dataframes[key].name==name:
                self.dataframes[key].activateDataframe(mode)
    def get_title_by_name(self, name)->str:
        for key in self.dataframes:
            if self.dataframes[key].name==name:
                return key
    def set_current(self,input):
        try:
            self.current=self.dataframes[input]
        except:
            try:
                for key in self.dataframes:
                    if self.dataframes[key].name==input:
                        self.current=self.dataframes[key]
                        return
            except:
                self.current=self.default
    def get_current(self)->dataset:
        return self.current
    def replace_current(self, dataframe):
        current=self.current
        title=current.title
        self.dataframes[title]=dataframe
        self.current=dataframe
        return