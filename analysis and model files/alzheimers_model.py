import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_excel('alzheimers_disease_data.xlsx')

print("Dataset Loaded Successfully")
print("Shape:", df.shape)
print(df.head())

print("\nDiagnosis Distribution:")
print(df['Diagnosis'].value_counts())

if df['Diagnosis'].dtype == 'object':
    df['Diagnosis'] = df['Diagnosis'].map({'No':0, 'Yes':1, 'Normal':0, 'Alzheimer':1})

plt.figure()

for label in df['Diagnosis'].unique():
    subset = df[df['Diagnosis'] == label]
    
    if label == 0:
        name = "Normal"
    else:
        name = "Alzheimer"
    
    plt.scatter(subset['MMSE'], subset['ADL'], label=name)

plt.xlabel('MMSE')
plt.ylabel('ADL')
plt.title('MMSE vs ADL (Alzheimer Detection)')
plt.legend()
plt.show()

plt.figure()

for label in df['Diagnosis'].unique():
    subset = df[df['Diagnosis'] == label]
    
    if label == 0:
        name = "Normal"
    else:
        name = "Alzheimer"
    
    plt.hist(subset['Age'], alpha=0.6, label=name)

plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Age Distribution by Diagnosis')
plt.legend()
plt.show()

plt.figure()

for label in df['Diagnosis'].unique():
    subset = df[df['Diagnosis'] == label]
    
    if label == 0:
        name = "Normal"
    else:
        name = "Alzheimer"
    
    plt.scatter(subset['Age'], subset['MMSE'], label=name)

plt.xlabel('Age')
plt.ylabel('MMSE')
plt.title('Age vs MMSE')
plt.legend()
plt.show()

features = ['MMSE', 'ADL', 'FunctionalAssessment', 'Age', 'SystolicBP', 'CholesterolLDL']
X = df[features]
y = df['Diagnosis']

X = X.fillna(X.mean())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)
log_pred = log_model.predict(X_test)

print("\n===== Logistic Regression =====")
print("Accuracy:", accuracy_score(y_test, log_pred))
print(classification_report(y_test, log_pred))

tree_model = DecisionTreeClassifier(max_depth=5, random_state=42)
tree_model.fit(X_train, y_train)
tree_pred = tree_model.predict(X_test)

print("\n===== Decision Tree =====")
print("Accuracy:", accuracy_score(y_test, tree_pred))
print(classification_report(y_test, tree_pred))

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

print("\n===== Random Forest =====")
print("Accuracy:", accuracy_score(y_test, rf_pred))
print(classification_report(y_test, rf_pred))

models = ['Logistic Regression', 'Decision Tree', 'Random Forest']
accuracies = [
    accuracy_score(y_test, log_pred),
    accuracy_score(y_test, tree_pred),
    accuracy_score(y_test, rf_pred)
]

plt.figure()
plt.bar(models, accuracies)
plt.xlabel('Models')
plt.ylabel('Accuracy')
plt.title('Model Comparison')
plt.show()

print("\nConfusion Matrix (Random Forest):")
print(confusion_matrix(y_test, rf_pred))

print("\nCorrelation with Diagnosis:")
print(df.corr(numeric_only=True)['Diagnosis'].sort_values(ascending=False))

print("\nModel Training Completed Successfully")