import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,classification_report
import pickle

#-------------------------- Load the data from the CSV file --------------------

dataset = pd.read_csv("with normalize.csv")
X_train = dataset.iloc[:, 1:-1]
Y=dataset['lable']
label_encoder = LabelEncoder()
X_train['Mobil-frindly'] = label_encoder.fit_transform(X_train['Mobil-frindly'])
X_train['image resulation'] = label_encoder.fit_transform(X_train['image resulation'])
X_train['contact info'] = label_encoder.fit_transform(X_train['contact info'])
print(X_train['image resulation'])
X_train, X_test, y_train, y_test = train_test_split(X_train, Y, test_size=0.3, random_state=42)

#--------------------------SVM--------------------------

# defining parameter range 
param_grid = {'C': [0.1, 1, 10, 100, 1000], 'gamma': [1, 0.1, 0.01, 0.001, 0.0001]}  
grid_search = GridSearchCV(SVC(kernel = 'rbf'), param_grid, refit = True, verbose = 3)

  
# fitting the model for grid search 
grid_search.fit(X_train, y_train)
print(grid_search.best_params_)
grid_pred = grid_search.predict(X_test)

print("The Report of the SVM :\n ", classification_report(y_test,grid_pred))

filename = 'SVM.sav'
pickle.dump(grid_search, open(filename, 'wb'))


