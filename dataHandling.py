#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 13:02:25 2023

@author: valcsevdaniel
"""
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from enum import Enum
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import mean_absolute_percentage_error
import numpy as np
#Formatting the data
dataset = pd.read_csv("Ingatlanok.csv")
HAS_ENCODING_FOR_AC = {
    "van" : True,
    "nincs" : False,
    "|nincs megadva|" : False
    }
HAS_ENCODING_FOR_ELEVATOR = {
    "van" : True,
    "nincs" : False
    }    
IS_ACCESIBBLE = {
    "igen" : True,
    "nem" : False
    }

def Parking_Parse(x):
    x = str(x).split()
    if len(x) >= 1:
        try:
            return float(x[0].replace(',', '.'))
        except:
            pass
        

def Level_Parse(x):
    if "földszint" in str(x):
        return 0
    else:
        try:
            return float(x)
        except:
            pass
def Building_Year_Parse(x):
    x = str(x).split()
    if len(x) >= 1:
        try:
            return int(x[0])
        except:
            pass
        

def Building_Level_Parse(x):
    x = str(x)
    if "földszintes" in x:
        return 0
    else:
        try:
            return int(x)
        except:
            return 0
def Isolation_Parse(x):
    x = str(x).split()
    try:
        return int(x[2])
    except:
        pass
    
def Inner_Height_Parser(x):
    x = str(x).split()
    try: 
        if "alacsonyabb" in x[-1]:
            return True
        elif "magasabb" in x[-1]:
            return False
        else:
            return math.nan
    except:
        pass


#dataset.rename(columns={'Belmagasság' : 'IsLessThan3Meters'}, inplace= True)
#dataset['Lift'] = dataset['Lift'].map(HAS_ENCODING_FOR_ELEVATOR)
dataset['Légkondicionáló'] = dataset['Légkondicionáló'].map(HAS_ENCODING_FOR_AC)
dataset['Légkondicionáló'].fillna(False,inplace=True)
dataset['Akadálymentesített'] = dataset['Akadálymentesített'].map(IS_ACCESIBBLE)
dataset['Akadálymentesített'].fillna(False, inplace=True)
#dataset['Parkolóhely ára']= dataset['Parkolóhely ára'].apply(lambda x : Parking_Parse(x))
#dataset['Emelet']= dataset['Emelet'].apply(lambda x : Level_Parse(x))
#dataset['Építés éve']= dataset['Építés éve'].apply(lambda x : Building_Year_Parse(x))
#dataset['Épület szintjei']= dataset['Épület szintjei'].apply(lambda x : Building_Level_Parse(x))
#dataset['Kertkapcsolatos']= dataset['Kertkapcsolatos'].map(IS_ACCESIBBLE)
dataset['Szigetelés']= dataset['Szigetelés'].apply(lambda x : Isolation_Parse(x))
median_value_szig = dataset['Szigetelés'].median()
dataset['Szigetelés'].isna().sum()
dataset['Szigetelés'].fillna(median_value_szig,inplace=True)
dataset['Komfort'].fillna("összkomfortos",inplace=True)
dataset["Ingatlan állapota"].fillna(method="ffill",inplace=True)
#dataset['IsLessThan3Meters'] = dataset['IsLessThan3Meters'].apply(lambda x : Inner_Height_Parser(x))





threshold = 200
filtered_dataset = dataset.dropna(thresh=len(dataset) - threshold, axis=1)
dataset = filtered_dataset
# Print the columns in the filtered DataFrame
print("Columns with less than 100 NaN values:")
print(filtered_dataset.columns)

obj = (dataset.dtypes == 'object')
object_cols = list(obj[obj].index)
print("Categorical variables:",len(object_cols))
 
int_ = (dataset.dtypes == 'int')
num_cols = list(int_[int_].index)
print("Integer variables:",len(num_cols))
 
fl = (dataset.dtypes == 'float')
fl_cols = list(fl[fl].index)
fl_cols = fl_cols + num_cols
print("Float and integer variables:",len(fl_cols))

plt.figure(figsize=(12, 6))
sns.heatmap(dataset[fl_cols].corr(),
            cmap='BrBG',
            fmt='.2f',
            linewidths=2,
            annot=True)

unique_values = []

dataset.dropna()
for col in object_cols:
  unique_values.append(dataset[col].unique().size)
plt.figure(figsize=(10,6))
plt.title('No. Unique values of Categorical Features')
plt.xticks(rotation=90)
sns.barplot(x=object_cols,y=unique_values)



s = (dataset.dtypes == 'object')
object_cols = list(s[s].index)
print("Categorical variables:")
print(object_cols)
print('No. of. categorical features: ', 
	len(object_cols))


OH_encoder = OneHotEncoder(sparse=False)
OH_cols = pd.DataFrame(OH_encoder.fit_transform(dataset[object_cols]))
OH_cols.index = dataset.index
OH_cols.columns = OH_encoder.get_feature_names_out()
df_final = dataset.drop(object_cols, axis=1)
df_final = pd.concat([df_final, OH_cols], axis=1)

X = df_final.drop(['price'], axis=1)
Y = df_final['price']
 
# Split the training set into 
# training and validation set
X_train, X_valid, Y_train, Y_valid = train_test_split(
    X, Y, train_size=0.8, test_size=0.2, random_state=0)

model_SVR = svm.SVR()
model_SVR.fit(X_train,Y_train)
Y_pred = model_SVR.predict(X_valid)
 
print(mean_absolute_percentage_error(Y_valid, Y_pred))

model_RFR = RandomForestRegressor(n_estimators=15)
model_RFR.fit(X_train, Y_train)
Y_pred = model_RFR.predict(X_valid)





 
print(mean_absolute_percentage_error(Y_valid, Y_pred))
