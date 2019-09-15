import pandas as pd
import json
from bs4 import BeautifulSoup
import requests

def convert(x):
    if x == 'false':
        return 0
    else:
        result = sum(list(map(int, x.split(' '))))
        return result
    
def takeg(x):
    return int(x[:-1])



with open('Ata/unpacked/Crops.json', 'r') as f:
    data = json.load(f)
f.close()
with open('Ata/unpacked/ObjectInformation.json', 'r') as f:
    data_info = json.load(f)
f.close()
info = pd.DataFrame(data_info['content'],index=[0])
info = info.T
crops = pd.DataFrame(data['content'],index=[0])
crops=crops.T
crops['Name'] = None
crops['Buy'] = None
crops['Sell Normal'] = None
crops['Sell Silver'] = None
crops['Sell Gold'] = None
crops['Growth'] = None
crops['Season'] = None
crops['Harvest'] = None
crops['Regrowth'] = None
crops['Harvest Method'] = None
crops['Extra Harvest'] = None
crops[0]=crops[0].apply(lambda x: x.split('/'))
idxs = list(crops.index.values)
for idx in idxs:
    crops.loc[idx,'Name'] = info.loc[idx,0].split('/')[0]
    crops.loc[idx,'Growth']= crops.loc[idx,0][0]
    crops.loc[idx,'Season']= crops.loc[idx,0][1]
    crops.loc[idx,'Harvest']= crops.loc[idx,0][3]
    crops.loc[idx,'Regrowth']= crops.loc[idx,0][4]
    crops.loc[idx,'Harvest Method']= crops.loc[idx,0][5]
    crops.loc[idx,'Extra Harvest']= crops.loc[idx,0][6]
crops = crops.drop(0,axis = 1)
crops['Harvest'] = crops['Harvest'].apply(lambda x: int(x))
crops['Harvest Method'] = crops['Harvest Method'].apply(lambda x: int(x))
crops['Regrowth'] = crops['Regrowth'].apply(lambda x: int(x))
crops['Harvest Mode'] = crops['Harvest Method'].apply(lambda x: 'Scythe' if x== 1 else 'Normal' )
crops['Regrowth'] = crops['Regrowth'].apply(lambda x: None if x == -1 else x)
crops['Growth'] = crops['Growth'].apply(lambda x: convert(x))
crops['Regrowth'] = crops['Regrowth'].apply(lambda x: int(x) if x/1==x  else 0)
crops.to_csv('Data/data.csv')
crops = crops.drop(['495','496','497','498'],axis=0)

def parse_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table')
    return tables
def parse_html_table(table):
    df = pd.read_html(str(table)) 
    return df

for i in range(2,109):
    try:
        url = 'https://stardewvalleywiki.com/Crops'
        tables = parse_url(url)
        df = parse_html_table(tables[i])
        name,surname = df[0]['Seeds'][0].split(' ')[:2]
        name += ' '
        name += surname
        buy  = float(df[0]['Seeds'][0].split(' ')[4][:-1])
        sells = df[0].loc[0,'Sells For'].split(' ')
        sells = list(map(takeg,sells))

        crops.loc[crops['Name']==name,'Buy'] = buy
        crops.loc[crops['Name']==name,'Sell Normal'] = sells[0]
        crops.loc[crops['Name']==name,'Sell Silver'] = sells[1]
        crops.loc[crops['Name']==name,'Sell Gold'] = sells[2]    
        print(i)
    except (KeyError,ValueError)as e:
        pass
    
#Rare Seeds
crops.loc['347','Buy'] = 1000
crops.loc['347','Sell Normal'] = 3000
crops.loc['347','Sell Silver'] = 3750
crops.loc['347','Sell Gold'] = 4500  

#Coffee Bean
crops.loc['433','Buy'] = 2500
crops.loc['433','Sell Normal'] = 15
crops.loc['433','Sell Silver'] = 18
crops.loc['433','Sell Gold'] = 20  

#Red Cabbage Seeds
crops.loc['485','Buy'] = 100
crops.loc['485','Sell Normal'] = 260
crops.loc['485','Sell Silver'] = 325
crops.loc['485','Sell Gold'] = 390

#Bok Choy Seeds
crops.loc['491','Buy'] = 50
crops.loc['491','Sell Normal'] = 80
crops.loc['491','Sell Silver'] = 100
crops.loc['491','Sell Gold'] = 120

#Ancient Seeds
crops.loc['499','Buy'] = 550
crops.loc['499','Sell Normal'] = 550
crops.loc['499','Sell Silver'] = 687
crops.loc['499','Sell Gold'] = 825

#Strawberry Seeds
crops.loc['745','Buy'] = 100
crops.loc['745','Sell Normal'] = 120
crops.loc['745','Sell Silver'] = 150
crops.loc['745','Sell Gold'] = 180

crops = crops.dropna()