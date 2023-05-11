import pandas as pd
from apps.common_items import *
import numpy as np
import plotly.express as px
class dataset:
    #Initiate your dataset. Column refers to the column in the dataframe that holds the numeric values. 
    #Group refers to the data that you wanna group, in case the data comes with filters. For example, you may wanna group the Household Income by County. 
    #The group and by arguments will allow the dataset to calculate the percent change version of the dataframe. 
    def __init__(self, title:str, df_original:pd.DataFrame, column=None, name=None, group=None, By=None, colors=None, groupMax=False, groupValue=None):
        #Every dataset will always keep the original dataframe. That way, operations don't cause issues for other operations. 
        self.df_original=df_original
        self.title=title
        self.groupMax=groupMax
        self.groupValue=groupValue
        if(column!=None):
            if(groupMax):
                #df_original.groupby(groupValue)
                self.max=df_original.groupby(groupValue).sum(numeric_only=True)[column].max()
                self.min=df_original.groupby(groupValue).sum(numeric_only=True)[column].min()
            else:
                self.max=df_original[column].max()
                self.min=df_original[column].min()
            self.valuePoint=column
        if(column==None):
            self.df_percent_change=None
           
        elif(column!=None and group!=None and By!=None):
            self.df_percent_change=self.get_percent_change(df_original, column, group, By)
        elif(column!=None and group==None and By==None):
            self.df_percent_change=self.get_percent_change_simple(column)
        self.df_active=df_original
        self.name=name
        self.active_mode='Original'
        self.trimMax=None
        self.trimMin=None
        self.trimmed=False
        self.unit=1
        if(colors!=None):
            self.colors=get_colors(df_original[colors].unique())
        else:
            self.colors=None
    #Provides the original dataframe without any modifications. 
    def get_original(self)->pd.DataFrame:
        return self.df_original
    #You can use this to fill dropdowns. It returns all possible options of a column and the default value. 
    def get_options(self,column:str):
        dff=self.df_original.copy()
        return [{'label':x,'value':x}for x in dff[column].unique()], dff[column].unique()[0]
    #Activates a view of the dataframe. Currently, it's either percent change or original. 
    def activateDataframe(self, mode):
        if(mode=='Original'):
            self.df_active=self.df_original
            self.active_mode='Original'
            self.unit=1
            self.trimmed=False
            self.trimMax=None
            self.trimMin=None
            if(self.valuePoint!=None):
                if(self.groupMax):
                #df_original.groupby(groupValue)
                    self.max=self.df_original.groupby(self.groupValue).sum(numeric_only=True)[self.valuePoint].max()
                    self.min=self.df_original.groupby(self.groupValue).sum(numeric_only=True)[self.valuePoint].min()
                else:
                    self.min=self.df_original[self.valuePoint].min()
                    self.max=self.df_original[self.valuePoint].max()
        if(mode=='PercentChange'):
            self.df_active=self.df_percent_change
            self.active_mode='PercentChange'
            self.unit=0.1
            self.trimmed=False
            self.trimMax=None
            self.trimMin=None
            if(self.valuePoint!=None):
                if(self.groupMax):
                #df_original.groupby(groupValue)
                    self.max=self.df_original.groupby(self.groupValue).sum(numeric_only=True)[self.valuePoint].max()
                    self.min=self.df_original.groupby(self.groupValue).sum(numeric_only=True)[self.valuePoint].min()
                else:
                    self.min=self.df_original[self.valuePoint].min()
                    self.max=self.df_original[self.valuePoint].max()
      #Returns the current active view of the dataset.   
    def getActive(self)->pd.DataFrame:
        df=self.df_active.copy()
        if(self.groupMax):
            df.groupby(self.groupValue)
        if(self.isTrimmed()):
            return df[(df[self.valuePoint]>=self.trimMin)&(df[self.valuePoint]<=self.trimMax)]
        return df
    #Returns the percent change view of the dataframe. 
    def get_percent_change(self, df, column, group, By)->pd.DataFrame:
        dff=df.copy()
        dff[column]=df[column].astype(float)
        dff[column]=df.groupby(group)[By].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
        #Pandas 1.4.3 -> 2.0. 
        
        return dff
    #
    def get_percent_change_simple(self, column):
        dff=self.df_original.copy()
        dff[column].pct_change()
        result=dff.copy()
        return result
    def get_active_mode(self)->str:
        return self.active_mode
    def modify_percent_change(self, filter, group, by):
        #Filter will be a column. For every element in that column, we'll do the percent change thing. So we have to filter one by one. 
        if(type(filter) is list):
            if(len(filter)==2):
                firstFilter=self.df_original[filter[0]].unique()
                secondFilter=self.df_original[filter[1]].unique()
                dataframes=[]
                for element in firstFilter:
                    for filtering in secondFilter:
                        dff=self.df_original[(self.df_original[filter[0]]==element) & (self.df_original[filter[1]]==filtering)]
                        df=dff.copy()
                        df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
                        dataframes.append(df)
                df_rest=pd.concat(dataframes)
                self.df_percent_change=df_rest
                return
            if(len(filter)==3):
                firstFilter=self.df_original[filter[0]].unique()
                secondFilter=self.df_original[filter[1]].unique()
                thirdFilter=self.df_original[filter[2]].unique()
                dataframes=[]
                for element in firstFilter:
                    for filtering in secondFilter:
                        for filteringTwo in thirdFilter:
                            dff=self.df_original.copy()
                            dff=dff[(dff[filter[0]]==element) & (dff[filter[1]]==filtering) & (dff[filter[2]==filteringTwo])]
                            df=dff.copy()
                            df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
                            dataframes.append(df)
                df_rest=pd.concat(dataframes)
                self.df_percent_change=df_rest
                return
            if(len(filter)==4):
                firstFilter=self.df_original[filter[0]].unique()
                secondFilter=self.df_original[filter[1]].unique()
                thirdFilter=self.df_original[filter[2]].unique()
                fourthFilter=self.df_original[filter[3]].unique()
                dataframes=[]
                for element in firstFilter:
                    for filtering in secondFilter:
                        for filteringTwo in thirdFilter:
                            for filteringThree in fourthFilter:
                                try:
                                    dff=self.df_original[(self.df_original[filter[0]]==element) & (self.df_original[filter[1]]==filtering) & (self.df_original[filter[2]==filteringTwo]) & (self.df_original[filter[3]==filteringThree])]
                                except:
                                    continue
                                df=dff.copy()
                                df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
                                dataframes.append(df)
                df_rest=pd.concat(dataframes)
                df_rest.replace([np.inf, -np.inf], 0, inplace=True)
                df_rest[by].replace(r'^\s*$',0)
                self.df_percent_change=df_rest
                return

        elements=self.df_original[filter].unique()
        dataframes=[]
        for element in elements:
            dff=self.df_original.copy()
            dff=dff[dff[filter]==element]
            df=dff.copy()
            df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
            dataframes.append(df)
        df_rest=pd.concat(dataframes)
        df_rest.replace([np.inf, -np.inf], 0, inplace=True)
        df_rest[by].replace(r'^\s*$',0)
        self.df_percent_change=df_rest
    def trim(self, max, min):
        if(max==self.max and min==self.min):
            self.reset()
            return
        if(max!=None):
            self.trimMax=max
        if(min!=None):
            self.trimMin=min
        self.trimmed=True
    def isTrimmed(self)->bool:
        return self.trimmed
    def reset(self):
        self.trimMax=None
        self.trimMin=None
        self.trimmed=False
    def getMin(self):
        return self.min
    def getMax(self):
        return self.max
    def getActiveMode(self)->str:
        return self.active_mode
    def adjustMinMax(self, column:str, value):
        if(type(column) is list and type(value) is list):
            if(len(column)==len(value)):
                df=self.df_active.copy()
                for i in range(0, len(column)):
                    df=df[df[column[i]]==value[i]]
                dff=df.copy()
                if(self.groupMax):
                    self.max=dff.groupby(self.groupValue).sum(numeric_only=True)[self.valuePoint].max()
                    self.min=dff.groupby(self.groupValue).sum(numeric_only=True)[self.valuePoint].min()
                else:    
                    self.min=dff[self.valuePoint].min()
                    self.max=dff[self.valuePoint].max()
                return 
            else:
                return None
        df=self.df_active.copy()
        df=df[df[column]==value]
        dff=df.copy()
        if(self.groupMax):
            self.max=dff.groupby(self.groupValue).sum(numeric_only=True)[self.valuePoint].max()
            self.min=dff.groupby(self.groupValue).sum(numeric_only=True)[self.valuePoint].min()
        else:
            self.min=dff[self.valuePoint].min()
            self.max=dff[self.valuePoint].max()
    def filter_dataset(self, column, value):
        if(self.active_mode=='Original'):
            dff=self.df_original
            self.df_active=dff[dff[column]==value]
        else:
            dff=self.df_percent_change
            self.df_active=dff[dff[column]==value]
    def adjust_colors(self, colors):
        if(len(colors)==len(self.colors)):
            return
        elif(len(colors)>len(self.colors)):
               for i in range(len(self.colors),len(colors)):
                r = lambda: random.randint(0,255)
                self.colors.append('#%02X%02X%02X' % (r(),r(),r()))
        elif(len(colors)<len(self.colors)):
            self.colors=self.colors[0:len(colors)]
    def get_line_chart(self, filters=None, values=None,colors=None, tick=None, dt=None):
        dff=self.getActive().copy()
        if(not filters==None):
            if(type(filters)=='list' and type(values)=='list'):
                for i in range(0, len(filters)):
                    dff=dff[dff[filters[i]==values[i]]]
            else:
                dff=dff[dff[filters]==values]
        fig=px.line(dff, x='Year', y=self.valuePoint, color=colors, color_discrete_sequence=get_colors(dff[colors].unique()))
        fig.update_xaxes(rangeslider_visible=True)
        if(not self.active_mode=='Original'):
            fig.update_yaxes(ticksuffix='%')
        if(tick!=None and dt!=None):
            fig.update_xaxes(tick0=tick, dtick=dt)
        return fig
    def test_maxmin(self):
        dff=self.df_original.copy()
        print(dff[self.valuePoint].max())
        print(dff[self.valuePoint].min())
    def get_columns(self)->list:
        return self.df_original.columns
    def get_title(self):
        return self.title
            
        

        
