import datetime
from os import path
import os
import requests
import bs4
import pandas as pd
import numpy as np
import warnings
import seaborn as sns
import plotly.express as px
import matplotlib.dates as mdates

warnings.filterwarnings("ignore")
formatter = mdates.DateFormatter('%b %d')


class ArmyLoss():
    
    def __init__(self):
        self.df = pd.DataFrame()
        self.base_url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year
        
        if path.exists("armyloss.pkl") and path.exists("armyloss_change.pkl"):
            
            self.df = pd.read_pickle("armyloss.pkl")
            
            self.new_df = pd.read_pickle("armyloss_change.pkl")
            
            if not self.df.iloc[-1]['Date'].day_of_year == pd.to_datetime("today").day_of_year:
                os.remove("armyloss.pkl")
                os.remove("armyloss_change.pkl")
            
        else:
            
            self.month_list = []
        
            self._update_month()
               
            self._fill_df()
        
            self._add_dates()
        
            self._pre_process() 
            
            self.df.to_pickle("armyloss.pkl")      
            
            self._preprocess_data_histplot()   
            
            self.new_df.to_pickle("armyloss_change.pkl")
 

    def _update_month(self):
        for year in range(2022, self.current_year + 1):
            if year == self.current_year:
                for month in range(1, self.current_month + 1): # add the current month
                    t = datetime.datetime(year, month, 1, 0, 0)
                    t = t.strftime('%Y-%m')
                    self.month_list.append(t)
            else:
                for month in range(2, 13): # add the current month
                    t = datetime.datetime(year, month, 1, 0, 0)
                    t = t.strftime('%Y-%m')
                    self.month_list.append(t)

            
    def _generate_resulset_data(self):
        for month in reversed(self.month_list):
            print(month)
            res = requests.get(self.base_url + month)
            soup = bs4.BeautifulSoup(res.text, 'html.parser');
            data = soup.find_all("div",{"class":"casualties"})
            self.result_set.extend(data[1:])
    
    def _fill_df(self):
        self.result_set = []
        self._generate_resulset_data()
        
        for i in reversed(range(len(self.result_set))):
            children = self.result_set[i].find_all("li")
            d = {}
            for child in children:
                list = child.getText().split()
                indx = list.index('—')
                name = []
                for j in range(indx):
                    name.append(list[j])
                name = " ".join(list[:indx])
                res = [int(ele) for ele in list if ele.isdigit()]
                d[name] = res[0]
            self.df = pd.concat([self.df, pd.DataFrame([d])], ignore_index = True)
            #self.df = self.df._append(d, ignore_index = True)
        
         
    
    
    def _generate_resultset_day(self):
        self.result_set = []
        for month in reversed(self.month_list):
            res = requests.get(self.base_url + month)
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            data = soup.find_all("span",{"class":"black"})
            self.result_set.extend(data[1:-1])
        
    def _add_dates(self):
        self.result_set = []
        self._generate_resultset_day()
        
        dates_list = []
        for i in reversed(range(len(self.result_set))):
            date = self.result_set[i].getText()
            dates_list.append(pd.Timestamp(day = int(date[0:2]), month = int(date[3:5]), year = int(date[6:]))) 
        
        self.df['Дата'] = dates_list
        
                    
    def _pre_process(self):
        self.df = self.df.fillna(0)
        self.df['Автомобілі'] = self.df["Автомобілі"] + self.df["Автомобілі та автоцистерни"] + self.df["Цистерни з ППМ"]
        self.df['РСЗВ'] = self.df['РСЗВ'] + self.df['РСЗВ Град']
        self.df = self.df.replace(0,np.nan)
        self.df = self.df.drop(columns = ['ЗРК БУК','РСЗВ Град','Автомобілі та автоцистерни','Цистерни з ППМ', 'Пускові установки ОТРК'])
        
        self.df = self.df.rename(columns = {
            'Літаки':'Fighter Aircrafts',
            'Танки':'Tanks',
            'Гелікоптери':'Helicopters',
            'БПЛА':'Unmanned Aircrafts',    
            'РСЗВ':'Multiple Rocket Launcher',
            'ББМ':'Armoured Vehicles',
            'Засоби ППО':'Air Defence Systems',
            'Гармати':'Artillery',
            'Особовий склад':'Manpower',
            'Кораблі (катери)':'Ships and Boats',
            'Крилаті ракети':'Cruise Missiles',
            'Автомобілі': 'Cars and Tank Cars',
            'Спеціальна техніка':'Special Equipment',
            'Дата': 'Date'
        })
        
    def get_columns(self):
        return self.df.columns.values.tolist()
    
    def get_linechart(self, labels):

        fig = px.line(self.df, x="Date", y=labels, title="Russia's military loss by days")
        
        fig.update_layout(
            title="Russia's military loss by days",
            xaxis_title="Date",
            yaxis_title="Count",
            font=dict(
                family="Courier New",
                size=16
            )
        )
    
        
        return fig
    
    def _pre_process_bar_plot(self,label):
        self.week_loss = []

        for i in range(0,len(self.df)-7,7):
            self.week_loss.append(self.df[label][i+7] - self.df[label][i])
        
        x = (len(self.df)-1)%7
        if x != 0:
            self.week_loss.append(self.df[label][self.df.index[-1]]-self.df[label][self.df.index[-1-x]])
            
    def get_bar_plot(self,label):        
        
        self._pre_process_bar_plot(label)
        
        array = np.array(self.week_loss)
        rank = array.argsort().argsort()
        week_num = np.linspace(1,len(self.week_loss),len(self.week_loss))
        week_num = [int(i) for i in week_num]

        fig = px.bar(x=week_num, y=self.week_loss)
        fig.update_layout(
            title="Bar chart of military losses per a week",
            xaxis_title="Week Number",
            yaxis_title="Count",
            font=dict(
                family="Courier New",
                size=16,
            )
        )
        
        return fig
    
    def get_recent_data(self, label):
        
        return int(self.df.iloc[-1][label]), int(self.df.iloc[-1][label] - self.df.iloc[-2][label])
    
    def _preprocess_data_histplot(self):
        self.new_df = self.df.diff()
        self.new_df['Date'] = self.df['Date']

            
    
    
    def get_box_plot(self, label):

        fig = px.scatter(self.new_df, x='Date', y=label, height = 600,  trendline="rolling",
                         trendline_options=dict(function="median", window=21))

        fig.update_traces(
            marker=dict(size=4)
        )
        fig.update_layout(
            title="Scatter plot of military losses per a day",
            xaxis_title="Date",
            yaxis_title="Count",
            font=dict(
                family="Courier New",
                size=14,
            )
        )
        
        return fig
    
    
if __name__ == "__main__":
    s = ArmyLoss()
        