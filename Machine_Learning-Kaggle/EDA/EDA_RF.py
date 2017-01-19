import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

print "Start"

dat_train = pd.read_csv("./raw/train.csv")
dat_test = pd.read_csv("./raw/test.csv")

ID = dat_test['id']

dat_test.drop('id', axis=1, inplace=True)
dat_train = dat_train.iloc[:, 1:]

# print dat_test.head(5)
# print dat_train.head(5)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

labels = []
split = 116
cols = dat_train.columns



for i in range(0,split):
    train = dat_train[cols[i]].unique()
    test = dat_test[cols[i]].unique()
    labels.append(list(set(train) | set(test)))
    # print "train"
    # print train
    # print "test"
    # print test
    # print "labels"
    # print labels

cats = []
for i in range(0, split):
    # print labels[i]
    #Label encode
    label_encoder = LabelEncoder()
    label_encoder.fit(labels[i])
    feature = label_encoder.transform(dat_train.iloc[:,i])
    # print feature
    feature = feature.reshape(dat_train.shape[0], 1)
    # print feature
    #One hot encode
    onehot_encoder = OneHotEncoder(sparse=False,n_values=len(labels[i]))
    feature = onehot_encoder.fit_transform(feature)
    # print feature
    cats.append(feature)

encoded_cats = np.column_stack(cats)
dataset_encoded = np.concatenate((encoded_cats,dat_train.iloc[:,split:].values),axis=1)
print "finished encoding"
print encoded_cats
# pd.DataFrame(dataset_encoded).to_csv("train_ONE_raw.csv", index=False)


#####################################
# CV setup
#####################################

print "CV split"
# dataset_encoded = pd.read_csv("train_ONE_raw.csv")

#get the number of rows and columns
r, c = dataset_encoded.shape

#create an array which has indexes of columns
i_cols = []
for i in range(0,c-1):
    i_cols.append(i)

#Y is the target column, X has the rest
X = dataset_encoded[:,0:(c-1)]
Y = dataset_encoded[:,(c-1)]
# del dataset_encoded

#Validation chunk size
val_size = 0.1

#Use a common seed in all experiments so that same chunk is used for validation
seed = 0

#Split the data into chunks
from sklearn import cross_validation
X_train, X_val, Y_train, Y_val = cross_validation.train_test_split(X, Y, test_size=val_size, random_state=seed)
del X
del Y

#All features
X_all = []

#List of combinations
comb = []

#Dictionary to store the MAE for all algorithms
mae = []

#Scoring parameter
from sklearn.metrics import mean_absolute_error

#Add this version of X to the list
n = "All"
#X_all.append([n, X_train,X_val,i_cols])
X_all.append([n, i_cols])

print X_all

#####################################
# Random Forest
#####################################

#Evaluation of various combinations of RandomForest

#Import the library
from sklearn.ensemble import RandomForestRegressor

#Add the n_estimators value to the below list if you want to run the algo
n_list = np.array([10, 50, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000])

for n_estimators in n_list:
    print n_estimators
    # Set the base model
    model = RandomForestRegressor(n_jobs=12,n_estimators=n_estimators,random_state=seed)

    algo = "RF"

    # Accuracy of the model using all features
    for name,i_cols_list in X_all:
        model.fit(X_train[:,i_cols_list],Y_train)
        result = mean_absolute_error(Y_val, model.predict(X_val[:,i_cols_list]))
        mae.append(result)
        print(name + " %s" % result)

    comb.append("%s" % n_estimators )

if (len(n_list)==0):
    mae.append(1213)
    comb.append("%s" % 50 )

print comb, mae

with open("RF_mae.txt", "w") as f:
    for c, e in zip(comb, mae):
        print >>f, "{},{}".format(c, e)
f.close()

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#Set figure size
plt.rc("figure", figsize=(25, 10))

#Plot the MAE of all combinations
fig, ax = plt.subplots()
plt.plot(mae)
#Set the tick names to names of combinations
ax.set_xticks(range(len(comb)))
ax.set_xticklabels(comb,rotation=45)
#Plot the accuracy for all combinations
plt.savefig("RF_2.png")

#Best estimated performance is 1213 when the number of estimators is 50