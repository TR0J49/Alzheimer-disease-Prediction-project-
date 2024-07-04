# -*- coding: utf-8 -*-
"""Alzheimer disease  project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TsMoRUjh2Tfk1rYXEUBmPzTQi-VJqgc5
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score

data = pd.read_csv('/content/alzheimers_disease_data.csv')

print(data.head())
data = data.drop(columns=['DoctorInCharge'])

data.shape

data.tail()

data.info()

data.describe()

data.isnull().sum()

"""# Correlation Matrix"""

for column in data.columns:
    try:
        data[column] = pd.to_numeric(data[column], errors='coerce')
    except ValueError:
        pass


data = data.dropna(axis=1, how='any')


corr_matrix = data.corr()

plt.figure(figsize=(16, 12))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix')
plt.show()

import numpy as np


# Generate sample data for different distributions
uniform_data = np.random.uniform(low=0, high=10, size=1000)
normal_data = np.random.normal(loc=0, scale=1, size=1000)
binomial_data = np.random.binomial(n=10, p=0.5, size=1000)
poisson_data = np.random.poisson(lam=3, size=1000)
lognormal_data = np.random.lognormal(mean=0, sigma=1, size=1000)
gamma_data = np.random.gamma(shape=2, scale=1, size=1000)
beta_data = np.random.beta(a=2, b=5, size=1000)

plt.figure(figsize=(12, 6))
sns.histplot(uniform_data, kde=True, color='blue')
plt.title('Uniform Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(normal_data, kde=True, color='green')
plt.title('Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(binomial_data, kde=True, color='red')
plt.title('Binomial Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(poisson_data, kde=True, color='purple')
plt.title('Poisson Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

# Plot log-normal distribution
plt.figure(figsize=(12, 6))
sns.histplot(lognormal_data, kde=True, color='orange')
plt.title('Log-normal Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(gamma_data, kde=True, color='brown')
plt.title('Gamma Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(beta_data, kde=True, color='pink')
plt.title('Beta Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

"""## Bar chart (Gender)"""

plt.figure(figsize=(12, 6))
sns.countplot(data=data, x='Gender')
plt.title('Bar Chart of Gender (0= Female , 1= Male)')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.show()

"""# Scatter Plot"""

plt.figure(figsize=(12, 6))
sns.scatterplot(data=data, x='Age', y='BMI', hue='Gender', palette='viridis')
plt.title('Scatter Plot of Age vs. BMI')
plt.xlabel('Age')
plt.ylabel('BMI')
plt.show()

"""# Histogram"""

# Histogram of a numerical variable (e.g., Age)
plt.figure(figsize=(12, 6))
sns.histplot(data['Age'], kde=True, color='skyblue')
plt.title('Histogram of Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(12, 12))
sns.pairplot(data[['Age', 'BMI', 'SystolicBP', 'DiastolicBP']])
plt.suptitle('Pairplot of Selected Variables', y=1.02)
plt.show()

"""# Laber Incoding\"""

label_encoder = LabelEncoder()
data['Diagnosis'] = label_encoder.fit_transform(data['Diagnosis'])

X = data.drop(columns=['Diagnosis'])
y = data['Diagnosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""# KNN"""

knn = KNeighborsClassifier()
param_grid = {'n_neighbors': [3, 5, 7, 9], 'weights': ['uniform', 'distance']}
grid_search = GridSearchCV(knn, param_grid, cv=5)
grid_search.fit(X_train, y_train)
best_knn = grid_search.best_estimator_

y_pred_knn = best_knn.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
conf_matrix_knn = confusion_matrix(y_test, y_pred_knn)
class_report_knn = classification_report(y_test, y_pred_knn)

print(f"KNN Accuracy: {accuracy_knn}")
print("KNN Confusion Matrix:")
print(conf_matrix_knn)
print("KNN Classification Report:")
print(class_report_knn)

plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix_knn, annot=True, fmt='d', cmap='Blues')
plt.title('KNN Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

if len(label_encoder.classes_) == 2:
    y_test_binarized = label_binarize(y_test, classes=[0, 1])
    y_score = best_knn.predict_proba(X_test)[:, 1]

    fpr, tpr, _ = roc_curve(y_test_binarized, y_score)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(10, 7))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

"""# Random Forest"""

rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
conf_matrix_rf = confusion_matrix(y_test, y_pred_rf)
class_report_rf = classification_report(y_test, y_pred_rf)

print(f"Random Forest Accuracy: {accuracy_rf}")
print("Random Forest Confusion Matrix:")
print(conf_matrix_rf)
print("Random Forest Classification Report:")
print(class_report_rf)

plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix_rf, annot=True, fmt='d', cmap='Blues')
plt.title('Random Forest Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

if len(label_encoder.classes_) == 2:
    y_score_rf = rf.predict_proba(X_test)[:, 1]

    fpr_rf, tpr_rf, _ = roc_curve(y_test_binarized, y_score_rf)
    roc_auc_rf = auc(fpr_rf, tpr_rf)

    plt.figure(figsize=(10, 7))
    plt.plot(fpr_rf, tpr_rf, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc_rf:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Random Forest Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

"""# Gradient Boosting"""

gb = GradientBoostingClassifier(random_state=42)
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)
accuracy_gb = accuracy_score(y_test, y_pred_gb)
conf_matrix_gb = confusion_matrix(y_test, y_pred_gb)
class_report_gb = classification_report(y_test, y_pred_gb)

print(f"Gradient Boosting Accuracy: {accuracy_gb}")
print("Gradient Boosting Confusion Matrix:")
print(conf_matrix_gb)
print("Gradient Boosting Classification Report:")
print(class_report_gb)

plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix_gb, annot=True, fmt='d', cmap='Blues')
plt.title('Gradient Boosting Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

if len(label_encoder.classes_) == 2:
    y_score_gb = gb.predict_proba(X_test)[:, 1]

    fpr_gb, tpr_gb, _ = roc_curve(y_test_binarized, y_score_gb)
    roc_auc_gb = auc(fpr_gb, tpr_gb)

    plt.figure(figsize=(10, 7))
    plt.plot(fpr_gb, tpr_gb, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc_gb:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Gradient Boosting Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

model_accuracies = {
    'KNN': accuracy_knn,
    'Random Forest': accuracy_rf,
    'Gradient Boosting': accuracy_gb
}

"""# Algo Comparison"""

plt.figure(figsize=(10, 7))
plt.bar(model_accuracies.keys(), model_accuracies.values(), color=['blue', 'green', 'red'])
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Model Accuracies Comparison')
plt.ylim(0, 1)
for i, (model, accuracy) in enumerate(model_accuracies.items()):
    plt.text(i, accuracy + 0.02, f'{accuracy:.2f}', ha='center')
plt.show()

"""# User Input"""

def get_user_input():
    user_data = []
    for column in X.columns:
        value = float(input(f"Enter value for {column}: "))
        user_data.append(value)
    return user_data


def predict_with_user_input(user_data):
    user_data = scaler.transform([user_data])
    prediction_knn = best_knn.predict(user_data)
    prediction_rf = rf.predict(user_data)
    prediction_gb = gb.predict(user_data)

    print(f"KNN Prediction: {label_encoder.inverse_transform(prediction_knn)}")
    print(f"Random Forest Prediction: {label_encoder.inverse_transform(prediction_rf)}")
    print(f"Gradient Boosting Prediction: {label_encoder.inverse_transform(prediction_gb)}")


user_data = get_user_input()
predict_with_user_input(user_data)