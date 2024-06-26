import pandas as pd
import numpy as np

import pickle

import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import MinMaxScaler

from sklearn.metrics import classification_report

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split


for i in range(5):
    print("sucessfull")

# Importing dataset
dataset = pd.read_csv('diabetes_Dataset.csv')

"""# Step 1: Descriptive Statistics"""

# Preview data
dataset.head()

# Dataset dimensions - (rows, columns)
dataset.shape

# Features data-type
dataset.info()

# Statistical summary
dataset.describe().T

# Count of null values
dataset.isnull().sum()

"""# Observations:

1.There are a total of 768 records and 9 features in the dataset.<br>
2.Each feature can be either of integer or float dataype.<br>
3.Some features like Glucose, Blood pressure , Insulin, BMI have zero values which represent missing data.<br>
4.There are zero NaN values in the dataset.<br>
5.In the outcome column, 1 represents diabetes positive and 0 represents diabetes negative.<br>



#Glucose Vs Outcome
plt.figure(figsize=(10,6))
sns.violinplot(data=dataset,x="Outcome",y="Glucose",split=True,inner="quart",linewidth=1)

#Glucose Vs BMI Vs Age
plt.figure(figsize=(20,10))
sns.scatterplot(data=dataset,x="Glucose",y="BMI" ,hue="Age",size="Age")

"""# Step 3: Data Preprocessing"""

dataset_new = dataset

# Replacing zero values with NaN
dataset_new[["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]] = dataset_new[["Glucose", "BloodPressure", "SkinThickness", "Insulin","BMI"]].replace(0,np.nan)

# Count of NaN
dataset_new.isnull().sum()

# Replacing NaN with mean values
dataset_new["Glucose"].fillna(dataset_new["Glucose"].mean(), inplace = True)
dataset_new["BloodPressure"].fillna(dataset_new["BloodPressure"].mean(), inplace = True)
dataset_new["SkinThickness"].fillna(dataset_new["SkinThickness"].mean(), inplace = True)
dataset_new["Insulin"].fillna(dataset_new["Insulin"].mean(), inplace = True)
dataset_new["BMI"].fillna(dataset_new["BMI"].mean(), inplace = True)

# Statistical summary
dataset_new.describe().T

# Feature scaling using MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
dataset_scaled = sc.fit_transform(dataset_new)

dataset_scaled = pd.DataFrame(dataset_scaled)

# Selecting features - [Glucose, Insulin, BMI, Age]
X = dataset_scaled.iloc[:, [1, 4, 5, 7]].values
Y = dataset_scaled.iloc[:, 8].values

# Splitting X and Y
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20, random_state = 42, stratify = dataset_new['Outcome'] )

# Checking dimensions
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("Y_train shape:", Y_train.shape)
print("Y_test shape:", Y_test.shape)

"""# Step 4: Data Modelling"""

# Logistic Regression Algorithm
logreg = LogisticRegression(random_state = 42)
logreg.fit(X_train, Y_train)

# Plotting a graph for n_neighbors

X_axis = list(range(1, 31))
acc = pd.Series()
x = range(1,31)

acc = []
for i in list(range(1, 31)):
    knn_model = KNeighborsClassifier(n_neighbors = i)
    knn_model.fit(X_train, Y_train)
    prediction = knn_model.predict(X_test)
    acc.append([metrics.accuracy_score(prediction, Y_test)])

# K nearest neighbors Algorithm
knn = KNeighborsClassifier(n_neighbors = 24, metric = 'minkowski', p = 2)
knn.fit(X_train, Y_train)

# Support Vector Classifier Algorithm
svc = SVC(kernel = 'linear', random_state = 42)
svc.fit(X_train, Y_train)

# Decision tree Algorithm
dectree = DecisionTreeClassifier(criterion = 'entropy', random_state = 42)
dectree.fit(X_train, Y_train)

# Random forest Algorithm
ranfor = RandomForestClassifier(n_estimators = 11, criterion = 'entropy', random_state = 42)
ranfor.fit(X_train, Y_train)

# Making predictions on test dataset
Y_pred_logreg = logreg.predict(X_test)
Y_pred_knn = knn.predict(X_test)
Y_pred_svc = svc.predict(X_test)
Y_pred_dectree = dectree.predict(X_test)
Y_pred_ranfor = ranfor.predict(X_test)

"""# Step 5: Model Evaluation"""

# Evaluating using accuracy_score metric
accuracy_logreg = accuracy_score(Y_test, Y_pred_logreg)
accuracy_knn = accuracy_score(Y_test, Y_pred_knn)
accuracy_svc = accuracy_score(Y_test, Y_pred_svc)
accuracy_dectree = accuracy_score(Y_test, Y_pred_dectree)
accuracy_ranfor = accuracy_score(Y_test, Y_pred_ranfor)

# Accuracy on test set
print("Logistic Regression: " + str(accuracy_logreg * 100))
print("K Nearest neighbors: " + str(accuracy_knn * 100))
print("Support Vector Classifier: " + str(accuracy_svc * 100))
print("Decision tree: " + str(accuracy_dectree * 100))
print("Random Forest: " + str(accuracy_ranfor * 100))


# Classification report
print(classification_report(Y_test, Y_pred_knn))

"""# Step 6: Model Deployment"""

pickle.dump(knn, open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))
