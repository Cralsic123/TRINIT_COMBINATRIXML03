# -*- coding: utf-8 -*-
"""crop_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fIcQ7rWrgSKTku5K0wkoAcpZ6dFzBh6G
"""

# importing the dependencies
import IPython
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv("Crop_recommendation.csv")
price = pd.read_csv("price.csv")

data.head(10)

price.head(5)

# checking the data shape
data.shape

# dropping duplicate
data.drop_duplicates()

# checking if there are null values
data.isnull().sum()

data.describe()

import plotly.express as px

fig = px.box(data, y="N", points="all")
fig.show()

fig = px.box(data, y="P", points="all")
fig.show()

fig = px.box(data, y="K", points="all")
fig.show()

# removing all outliers

def del_out(data1, str):
    df_boston = data1
    df_boston.columns = df_boston.columns
    df_boston.head()

    Q1 = np.percentile(df_boston[str], 25, interpolation = 'midpoint')
    Q3 = np.percentile(df_boston[str], 75, interpolation = 'midpoint')

    IQR = Q3 - Q1
    
    print("old Shape: ", df_boston.shape)

    upper = np.where(df_boston[str] >= (Q3+1.5*IQR))
    lower = np.where(df_boston[str] <= (Q1 - 1.5*IQR))

    df_boston.drop(upper[0], inplace = True)
    df_boston.drop(lower[0], inplace = True)

    print("New shape: ", df_boston.shape)
    return df_boston

data = del_out(data, "rainfall")
data = del_out(data, "K")

"""now we will implement correlation"""

#import random
#from Ipython.core.display import update_display

data.corr()

# now we will create a correlation heatmap

fig,ax = plt.subplots(1,1,figsize=(15,9))
sns.heatmap(data.corr(),annot=True,cmap='Wistia')
ax.set(xlabel = 'features')
ax.set(ylabel = 'features')

plt.title("feature correlation", fontsize = 18, c="green")
plt.show

X = data.drop('label',axis = 1)
Y = data['label']

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.30,shuffle=True,random_state=0)

from sklearn.metrics import accuracy_score

clf = RandomForestClassifier()
clf.fit(x_train, y_train)

# Predict on the test data
y_pred = clf.predict(x_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Random forest classifier Accuracy:", accuracy)

from sklearn.metrics import confusion_matrix
matrix = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(15,15))
sns.heatmap(matrix, annot = True, fmt=".0f", linewidths = .5, square = True, cmap = 'Blues');
plt.ylabel('Actual label')
plt.xlabel('Predicted label');
sam_title = "Confusion Matrix - Score: "+ str(accuracy_score(y_test,y_pred))
plt.title(sam_title,size = 15);
plt.show()

x_test[3:4]

def prediction(a,b,c,d,e,f,g):
    result = clf.predict([[a,b,c,d,e,f,g]])
    return result

result1 = prediction(60,	38,	17,	18.41933,	64.235803,	6.474477,	76.413124)
#'22','17','5','24.121887','90.7235','6.945563','102.835632'
print(result1[0])

y_test[3:4]

# we are saving the model to create a webapp
import pickle
pickle.dump(clf, open("crop_predictor.pkl","wb"))

"""Now we are dealing with the price dataset"""

price.head(5)

price = price[['state','district','market','commodity', 'variety','max_price']]

price.head(5)

def get_crop_details(crop_name):
    # Filter the DataFrame to get only the rows where crop_name matches the input
    filtered_df = price[price['commodity'] == crop_name]
    # Get the max price for the crop
    max_price = filtered_df['max_price'].max()
    
    # Filter the DataFrame again to get only the rows where max_price matches the max price we found
    result = filtered_df[filtered_df['max_price'] == max_price]
    # Get the attributes corresponding to the max price
    city = result['state'].values[0]
    district = result['district'].values[0]
    market = result['market'].values[0]
    variety = result['variety'].values[0]
    
    # Print the result
    print(f"The max price for {crop_name} is {max_price} and it is found in {city}, {district}")

# Example usage
print(result1[0])
get_crop_details(result1[0])

