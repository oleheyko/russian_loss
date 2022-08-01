import datetime
from os import path
import requests
import bs4
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
formatter = mdates.DateFormatter('%b %d')

class ArmyLoss():
    
    def __init__(self):
        self.df = pd.DataFrame()
        self.base_url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
        self.current_month = datetime.datetime.now().month 
        
        if not path.exists("armyloss.pkl"):
            
            self.month_list = []
        
            self._update_month()
               
            self._fill_df()
        
            self._add_dates()
        
            self._pre_process()
            
            self.df.to_pickle("armyloss.pkl")
            
        else:
            
            self.df = pd.read_pickle("armyloss.pkl")
            
        
#        self._generate_resultset_day()
        
    def _update_month(self):
        for i in range(2,self.current_month + 1): # add the current month
            t = datetime.datetime(2022, i, 1, 0, 0)
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
            self.df = self.df.append(d, ignore_index = True)
    
    
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
            'БПЛА':'Unamanned Aircrafts',    
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
        font2 = {'family':'serif','color':'black','size':18}
        
        f, ax = plt.subplots(figsize=(8, 8))
        f.patch.set_facecolor('white')
        for item in labels:
            ax.plot(self.df['Date'], self.df[item],label = item)
        plt.grid()
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        ax.xaxis.set_major_formatter(formatter)
        ax.tick_params(axis='x', rotation=45,  width=2)
        ax.legend()
        plt.xlabel("Day",fontdict = font2)
        plt.ylabel("Number", fontdict = font2)
        
        return f