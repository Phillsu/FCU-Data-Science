import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

#字體設定
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['font.serif'] = ['Arial Unicode MS']

#讀入檔案
path1 = "/Users/mac/Documents/DataScience/midproject/10912.json"
path2 = "/Users/mac/Documents/DataScience/midproject/交通事故代號.csv"
with open(path1, 'r', encoding='utf-8') as file:
    tmp = pd.DataFrame(json.load(file))
df = tmp[['時', '區', '死', '受傷','GPS緯度','GPS經度', '飲酒情形', '主要肇因', '事故位置']]
#dfcmp比對代號用
dfcmp = pd.DataFrame(pd.read_csv(path2))
dfcmp = dfcmp.fillna('')
#1.事故發生=========================================================
#區域死傷(長條圖)
area = list(df['區'])
died = list(df['死'])
injured = list(df['受傷'])
while '' in area:
    area.remove('')
#如為空則為0
for i in range(len(died)):
    if(died[i] == ''):
        died[i] = 0
    died[i] = int(died[i])
    
for i in range(len(injured)):
    if(injured[i] == ''):
        injured[i] = 0
    injured[i] = int(injured[i])
#統計區域死傷
dic = {}
for i in range(len(area)):
    if(area[i] not in dic):
        dic[area[i]] = [0,0]
    dic[area[i]][0] += died[i]
    dic[area[i]][1] += injured[i]

area = list(dic.keys())
value = list(dic.values())
died = []
injured = []
for i in range(len(value)):
    injured.append(value[i][1])
    died.append(value[i][0])
    
#繪製圖表
plt.figure(figsize = (25, 12))
plt.bar(np.arange(len(dic)), injured, label = '受傷', color = 'steelblue', alpha = 0.8, width = 0.45)
plt.bar(np.arange(len(dic))+0.45, died, label = '死亡', color = 'indianred', alpha = 0.8, width = 0.45)
plt.xticks(np.arange(len(dic))+0.45,area, fontsize = 20, rotation='vertical')
plt.yticks(fontsize = 20)
plt.xlabel("區域", fontweight = "bold", fontsize = 20)                  
plt.ylabel("數量", fontweight = "bold", fontsize = 20)   
plt.title("12月區域死亡/受傷",fontsize = 15, fontweight = "bold")
for x,y in enumerate(injured):plt.text(x,y,'%s'%y,ha='center')
for x,y in enumerate(died):plt.text(x+0.45,y,'%s'%y,ha='center')
plt.legend(fontsize = 30)
plt.show()
#事故散布圖===========================================================
x=list(df['GPS經度'])
y=list(df['GPS緯度'])
#刪除空資料
for i in range(len(x)-1, -1, -1):
    if x[i] == '' or y[i] == '':
        x.pop(i)
        y.pop(i)
    else:
        x[i] = float(x[i])
        y[i] = float(y[i])
#製圖
plt.figure(figsize=(25, 13))
plt.xlabel('GPS經度', fontweight = "bold", fontsize=20)
plt.ylabel('GPS緯度', fontweight = "bold", fontsize=20)
plt.title('台中事故發生散布圖({}筆)'.format(len(x)), fontweight = "bold", fontsize=25)
plt.scatter(y, x, s=5, c='m', alpha=0.5, marker = "D")
plt.show()

#計算區域事故數量=====================================================
#計算區域事故數(長條圖)
area = {}
for i in df['區']:
    if i == '':
        continue
    if i not in area:
        area[i] = 1
    else :
        area[i] = area[i]+1
#series降冪排序
area = pd.Series(area, index = area.keys())
area = area.sort_values(ascending = False)
plt.figure(figsize=(25,13))   
#製圖
for i,j in enumerate(area):
    plt.text(i,j,'%s'%j,ha='center')
plt.style.use("ggplot")
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.xlabel("數量", fontweight = "bold", fontsize = 20)                  
plt.ylabel("區域", fontweight = "bold", fontsize = 20)   
plt.title("區域事故數({}筆)".format(sum(area)),fontsize = 20, fontweight = "bold")
area.plot.bar()
plt.show()
#======================================================================
#2. 飲酒與事故關系(圓餅圖)
#字典統計每種酒測狀況
data = list(df['飲酒情形'])
while '' in data:
    data.remove('')
temp = len(data)
dic = {}
for i in data:
    if i not in dic:
        dic[i] = 1
    else :
        dic[i] = dic[i]+1
data = pd.Series(dic)
data = data.sort_values(ascending = False)
'''
cmp = list(dfcmp['飲酒情形'])
while '' in cmp:
    cmp.remove('')
print(cmp)
'''
#資料有缺所以上網找代號
cmp = ['1經觀察未飲酒','2經檢測無酒精反應','3經呼氣檢測未超過 0.15 mg/L或血液檢測未超過 0.03%','4經呼氣檢測 0.16~0.25 mg/L或血液檢測 0.031%~0.05%','5經呼氣檢測 0.26~0.40 mg/L或血液檢測 0.051%~0.08%','6經呼氣檢測 0.41~0.55 mg/L或血液檢測 0.081%~0.11%','7經呼氣檢測 0.56~0.80 mg/L或血液檢測 0.111%~0.16%','8經呼氣檢測超過 0.80 mg/L或血液檢測超過 0.16%','9無法檢測','10非駕駛人，未檢測','11不明']
idx = []
labels = []
for i in data.keys():
    for j in cmp:
        if j.find(str(i))==0:
            labels.append(j)
            idx.append(i)
            break
#將數量較少的後五個歸類為其他，保持圖表整潔
data = list(data)
temp = sum(data[-6:])
del(data[-6:])
data.append(temp)
del(idx[-6:])
idx.append('其他')
del(labels[-6:])
labels.append('其他')
plt.figure(figsize = (25, 13)) 
plt.title("飲酒情形({}筆)".format(temp),fontsize = 20, fontweight = "bold")
plt.pie(data, labels = idx, autopct = '%1.1f%%')
plt.legend(labels, loc='upper right', fontsize = 16)
plt.show()
#=====================================================================
#3.事故發生時間趨勢圖
data = [0]*24
for i in df['時']:
    if i != '':
        data[int(i)]+=1

plt.figure(figsize = (25, 13))
plt.xticks(range(24), fontsize = 20)
plt.yticks(fontsize = 20)
plt.xlabel("時", fontweight = "bold", fontsize = 20)                  
plt.ylabel("事故數量", fontweight = "bold", fontsize = 20, rotation = 90)   
plt.title("12月事故發生時間分布({}筆)".format(sum(data)),fontsize = 20, fontweight = "bold")
plt.plot(data, c = 'b', marker = 'o')
plt.show()

#=====================================================================
#5.事故發生種類(長條圖)
cmp = list(dfcmp['肇事因素'])
while '' in cmp:
    cmp.remove('')
idx = []
labels = []
#比對代號
for i in df['主要肇因']:
    if i == '':
        continue
    if int(i) < 10:
            i = '0'+str(i)
    for j in cmp:
        if j.find(str(i))==0:
            idx.append(i)
            break
c = len(idx)
rank = []
count = []
#取得數量前三
for i in range(3):
    temp = max(idx,key=idx.count)
    count.append(idx.count(temp))
    rank.append(temp)
    while temp in idx:
        idx.remove(temp)
#製作圖表文字串列 labels
for i in rank:
    if i == '':
        continue
    for j in cmp:
        if j.find(str(i))==0:
            j = j.replace(str(i), '')
            labels.append(j)
            break
#製圖
plt.figure(figsize = (25, 13))
plt.xticks(range(3), labels, fontsize = 20)
plt.yticks(fontsize = 20)
plt.xlabel("肇事主因", fontweight = "bold", fontsize = 20)                  
plt.ylabel("事故數量", fontweight = "bold", fontsize = 20)   
plt.bar(range(3), count)
plt.title("肇事主因前三名({}筆)".format(c),fontsize = 20, fontweight = "bold")
plt.show()
#6.事故發生位置(哪種路段)=====================================================
cmp = list(dfcmp['事故位置'])
#移除空資料
while '' in cmp:
    cmp.remove('')
#比對代號
idx = []
labels = []
for i in df['事故位置']:
    if i == '':
        continue
    if int(i) < 10:
            i = '0'+str(i)
    for j in cmp:
        if j.find(str(i))==0:
            idx.append(i)
            break
c = len(idx)
#取得數量前三
rank = []
count = []
for i in range(5):
    temp = max(idx,key=idx.count)
    count.append(idx.count(temp))
    rank.append(temp)
    while temp in idx:
        idx.remove(temp)
#製作圖表文字串列 labels
for i in rank:
    for j in cmp:
        if j.find(str(i))==0:
            j = j.replace(str(i), '')
            labels.append(j)
            break
#製圖
plt.figure(figsize = (25, 13))
plt.xticks(range(5), labels, fontsize = 20)
plt.yticks(fontsize = 20)
plt.ylabel("事故數量", fontweight = "bold", fontsize = 20)
plt.xlabel("事故位置", fontweight = "bold", fontsize = 20)   
plt.bar(range(5), count)
plt.title("事故位置排行前五名({}筆)".format(c),fontsize = 20, fontweight = "bold")
plt.show()