import pandas as pd
import numpy as np
import csv
#Load the dataset from CSV file.
data = pd.read_csv("Website_dataset.csv")
# Take only features colimn, exclude URL column.
data = data.iloc[:, 1:]

from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# encode categorical features to numerical.
lb_make = LabelEncoder()
data['Mobile-UI'] = lb_make.fit_transform(data['Mobile-UI'].astype('str'))
data['High resolution photos'] = lb_make.fit_transform(data['High resolution photos'].astype('str'))
data['Contact informations'] = lb_make.fit_transform(data['Contact informations'].astype('str'))

# Normalization
scaler = StandardScaler()
data = scaler.fit_transform(data)

# Using KMeans built-in function with 5 clusters and fit the data on it.
kmeans = KMeans(n_clusters=5)
kmeans.fit(data)
# Predict lables of the data
labels = kmeans.predict(data)
centroids = kmeans.cluster_centers_
i=2
# Print labels.
for label in labels:
    print(i,label)
    i = i+1
