# -*- coding: utf-8 -*-
"""q1_ANN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a5q0wCol4gmd7VIUyhsaeebJUpdmmgdP
"""

!wget https://archive.ics.uci.edu/ml/machine-learning-databases/connect-4/connect-4.data.Z
!uncompress connect-4.data.Z


import urllib.request
import gzip
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import randint
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split, RandomizedSearchCV

# Define mapping for 'b', 'o', and 'x'
mapping = {'b': 0, 'o': 1, 'x': 2}

# Read dataset and replace values with integers
df = pd.read_csv('connect-4.data', header=None)
df.replace(mapping, inplace=True)

# Define mapping for 'won', 'loss', and 'draw'
outcome_mapping = {'win': 1, 'loss': 0, 'draw': 2}

# Replace outcome values with integers
df.replace(outcome_mapping, inplace=True)



#df = pd.read_csv('connect-4.data', header=None)



# Separate the target variable from the rest of the data
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# Create an ANN classifier
ann_clf = MLPClassifier()
ann_clf.fit(X_train, y_train)
y_pred = ann_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy_ann_clf: ', accuracy)
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

scores = cross_val_score(ann_clf, X_train, y_train, cv=5, n_jobs=-1)
# Print the cross-validation scores
print('Cross-Validation Scores: ', scores)

# Define the hyperparameters for grid search
param_grid = {
    'hidden_layer_sizes': [(100,), (100, 50), (50,)],
    'activation': ['relu', 'tanh', 'logistic'],
    'solver': ['adam', 'sgd'],
    'alpha': [0.0001, 0.001, 0.01]
}

# Perform grid search with cross-validation
grid_search = GridSearchCV(ann_clf, param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Print the best hyperparameters and score
print('Best Hyperparameters: ', grid_search.best_params_)
print('Best Score: ', grid_search.best_score_)
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Calculate the evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy_grid: ', accuracy)
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))


# Create an ANN classifier with best hyperparameters
ann_clf = MLPClassifier(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', alpha=0.0001)

# Evaluate the ANN classifier using k-fold cross-validation
scores = cross_val_score(ann_clf, X_train, y_train, cv=5, n_jobs=-1)
# Print the cross-validation scores
print('Cross-Validation Scores: ', scores)
ann_clf.fit(X_train,y_train)
# Make predictions on the test set
y_pred = ann_clf.predict(X_test)

# Calculate the evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy of best: ', accuracy)
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1-score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))