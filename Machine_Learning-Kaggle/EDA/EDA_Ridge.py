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

print dataset_encoded.shape
#get the number of rows and columns
r, c = dataset_encoded.shape

#create an array which has indexes of columns
i_cols = []
for i in range(0,c-1):
    i_cols.append(i)

#Y is the target column, X has the rest
X = dataset_encoded[:,0:(c-1)]
Y = dataset_encoded[:,(c-1)]
del dataset_encoded

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
# Ridge
#####################################
print "Ridge start"

#Import the library
from sklearn.linear_model import Ridge

#Add the alpha value to the below list if you want to run the algo
# a_list = np.array([100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001])
power = np.linspace(4, -3, 15)
a_list = [10**i for i in power]

print "=" * 50
print Y_val
print "=" * 50

for alpha in a_list:
    print alpha
    #Set the base model
    model = Ridge(alpha=alpha,random_state=seed)

    algo = "Ridge"
    # print X_train
    #Accuracy of the model using all features
    for name,i_cols_list in X_all:
        model.fit(X_train[:,i_cols_list],Y_train)
        result = mean_absolute_error(Y_val, model.predict(X_val[:,i_cols_list]))
        mae.append(result)
        print(name + " %s" % result)

    comb.append(" %s" % alpha)

#Result obtained by running the algo for alpha=0.001
if (len(a_list)==0):
    mae.append(1262.5)
    comb.append(" %s" % 0.001 )

print comb, mae

with open("Ridge_mae.txt", "w") as f:
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
# ax.xlabel("lambda")
# ax.ylabel("MAE")
#Plot the accuracy for all combinations
# plt.show()
plt.savefig("Ridge_2.png")

#High computation time
#Best estimated performance is 1308.1 for alpha = 1.0
