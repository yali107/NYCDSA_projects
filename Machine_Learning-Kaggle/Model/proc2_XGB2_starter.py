import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.cross_validation import KFold
import xgboost as xgb
# from xgboost import XGBRegressor

print "Start"

SEED = 0

shift = 200
train = pd.read_csv("train_proc2.csv")
X = train.iloc[:, 1:-1]
y = np.log(train.iloc[:, -1] + shift)

test = pd.read_csv("test_proc2.csv")
X_test = test.iloc[:, 1:-1]
# y_test = np.log(test.iloc[:, -1] + shift)

print X.head()
print X_test.head()

# n_train = train.shape[0]
# train_test = pd.concat((train, test)).reset_index(drop=True)
#
# print "train_test"
# print train_test.head()

def xg_eval_mae(preds, dtrain):
    labels = dtrain.get_label()
    return 'mae', mean_absolute_error(np.exp(preds), np.exp(labels))

xgtrain = xgb.DMatrix(X, label=y)
xgtest = xgb.DMatrix(X_test)

params = {
    'min_child_weight': 1,
    'eta': 0.01,
    'colsample_bytree': 0.5,
    'max_depth': 12,
    'subsample': 0.8,
    'alpha': 1,
    'gamma': 1,
    'silent': 1,
    'verbose_eval': True,
    'seed': SEED
}

# res = xgb.cv(params, xgtrain, num_boost_round=3000, nfold=10, seed=SEED, stratified=False,
#              early_stopping_rounds=15, verbose_eval=10, show_stdv=True, feval=xg_eval_mae, maximize=False)
#
# print res
#
# best_nrounds = res.shape[0] - 1
# print "-" * 50
# print best_nrounds
# print "-" * 50
# cv_mean = res.iloc[-1, 0]
# cv_std = res.iloc[-1, 1]
# print 'cv means: {} {}'.format(cv_mean, cv_std)

gbdt = xgb.train(params, xgtrain, 2235, feval=xg_eval_mae)
# print gbdt
# print gbdt.predict(xgtest)

print "outputting"
subm = pd.DataFrame()
# print np.exp(gbdt.predict(xgtest)) + shift
subm["loss"] = np.exp(gbdt.predict(xgtest)) + shift
print subm
subm.to_csv("proc2_XGB2_starter.csv", index=None)

###############################################################
# train_full = pd.read_csv("./Processed1/train_full.csv")
# X_full = train_full.iloc[:, :-1]
# y_full = np.log(train_full.iloc[:, -1] + shift)
# print y
#
# test_sub = pd.read_csv("./Processed1/submit.csv")
# X_sub = test_sub
#
# xgtrain_full = xgb.DMatrix(X_full, label=y_full)
# xgtest_sub = xgb.DMatrix(X_sub)
#
# overall_model = xgb.train(params, xgtrain_full, best_nrounds, feval=xg_eval_mae)
#
# print "outputting overall"
# submission = pd.DataFrame()
# # print np.exp(gbdt.predict(xgtest)) + shift
# submission["loss"] = np.exp(overall_model.predict(xgtest_sub)) + shift
# print subm
# submission.to_csv("proc_s_XGB2_tAll.csv", index=None)
