"""
RF - gesture classification model
"""

########################
# IMPORT
########################
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import time

########################
# DATA PREPARATION
########################

# Read in the original dataset
all_data = pd.read_csv('original_copy.csv', header = None)

# Choose a seed
seed = 12345
np.random.seed(seed)

# Create variable names (lables) and target name
count = 1
labellist = []

while count <= 128:
    string = "electrode_"
    string += str(count)
    labellist.append(string)
    count += 1

labellist.append("gesture")
del(count, string)

# Change column names
all_data.columns = labellist

# Add an ID column
all_data.insert(0, 'id', range(1, 1 + len(all_data)))

# Identify inputs and the target variable
x = all_data[labellist[:-1]]
y = all_data["gesture"]

# Split into training and validation (test) datasets. Ratio: 70/30
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.3, random_state = seed)

########################
# BASIC MODEL
########################

clf_basic = RandomForestClassifier(n_estimators = 100, random_state = seed)
clf_basic.fit(x_train, y_train)
y_pred = clf_basic.predict(x_test)

# Accuracy
accuracy = metrics.accuracy_score(y_test, y_pred)
print("Accuracy on the training set: ", accuracy)

########################
# PARAMETER TUNING
########################

# Setup the parameters and distributions to sample from: param_dist

param_dist = {"n_estimators": [500], # 500, 1000], #[100, 200],
              "max_depth": [72], #np.arange(10, 75),
              "max_features": [3], #randint(1, 12), # np.arange(1, 12), #randint(1, 12)
              "min_samples_leaf": [0.001], #randint(0.01, 0.1), #[100], #[100, 200, 300, 400, 500],
              "min_samples_split": [4],
              "n_jobs": [-1],
              "criterion": ["gini"]} #"gini", "entropy"]}

print ('start fitting')             # Change this later to write to log
clf = RandomForestClassifier(n_estimators = 500, min_samples_leaf=0.00075, max_features=3, 
                             criterion = "gini", 
                             random_state = seed, n_jobs = -1) # max depth not needed,

# Fit the RF model
clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)

y_pred_train = clf.predict(x_train)
accuracy = metrics.accuracy_score(y_train, y_pred_train)
print("Accuracy train: ", accuracy)

accuracy = metrics.accuracy_score(y_test, y_pred)
print("Accuracy on the test set: ", accuracy)       
