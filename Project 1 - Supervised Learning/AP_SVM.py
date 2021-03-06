import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import svm
import os
from textwrap import wrap

df = pd.read_csv('datasets/AP_Analytics.csv', delimiter=',', quotechar='"')

if(not os.path.exists('plots')):
    dirname = 'plots'
    os.mkdir(dirname)
    dirname = 'AP_Analytics'
    os.mkdir('plots/%s' %dirname)

if(not os.path.exists('plots/AP_Analytics')):
    dirname = 'AP_Analytics'
    os.mkdir('plots/%s' %dirname)
    dirname = 'SVM'
    os.mkdir('plots/AP_Analytics/%s' %dirname)

if(not os.path.exists('plots/AP_Analytics/SVM')):
    dirname = 'SVM'
    os.mkdir('plots/AP_Analytics/%s' %dirname)


df = pd.get_dummies(df)

X = df.ix[:, df.columns != 'Chance of Admit ']
y = df['Chance of Admit ']


X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.30, random_state=30)

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#SVM_rbf
train_size = len(X_train)
offsets = range(int(0.1 * train_size), train_size, int(0.05 * train_size))
train_err = [0] * len(offsets)
test_err = [0] * len(offsets)
train_size = len(X_train)

for i, o in enumerate(offsets):
    print 'SVM: learning an SVM(kernel = rbf) with training_set_size=' + str(o)
    clf = svm.SVC(C=1.0, degree=3, gamma='auto', kernel='rbf')
    X_train_temp = X_train[:o].copy()
    y_train_temp = y_train[:o].copy()
    X_test_temp = X_test[:o].copy()
    y_test_temp = y_test[:o].copy()
    clf.fit(X_train_temp, y_train_temp)
    train_err[i] = mean_squared_error(y_train_temp,
                                     clf.predict(X_train_temp))
    test_err[i] = mean_squared_error(y_test_temp,
                                    clf.predict(X_test_temp))
    print 'train_err: ' + str(train_err[i])
    print 'test_err: ' + str(test_err[i])
    print '---'

# Plot results
print 'plotting results'
plt.figure()
title = 'AP Analytics SVM(kernel = rbf): Performance x Training Set Size'
plt.title('\n'.join(wrap(title,60)))
plt.plot(offsets, test_err, '-', label='test error')
plt.plot(offsets, train_err, '-', label='train error')
plt.legend()
plt.xlabel('Num Estimators')
plt.ylabel('Mean Square Error')
plt.savefig('plots/AP_Analytics/SVM/APAnalytics_rbf_PerformancexTrainingSetSize.png')
print 'plot complete'
### ---


#SVM_linear
train_size = len(X_train)
offsets = range(int(0.1 * train_size), train_size, int(0.05 * train_size))
train_err = [0] * len(offsets)
test_err = [0] * len(offsets)
train_size = len(X_train)
c_coefs = [0.1, 1]

for c in c_coefs:
    for i, o in enumerate(offsets):
        print 'SVM: learning an SVM(kernel = linear) with training_set_size = ' + str(o) + ' and c = ' + str(c)
        clf = svm.SVC(C=c, degree=3, gamma='auto', kernel='linear')
        X_train_temp = X_train[:o].copy()
        y_train_temp = y_train[:o].copy()
        X_test_temp = X_test[:o].copy()
        y_test_temp = y_test[:o].copy()
        clf.fit(X_train_temp, y_train_temp)
        train_err[i] = mean_squared_error(y_train_temp,
                                         clf.predict(X_train_temp))
        test_err[i] = mean_squared_error(y_test_temp,
                                        clf.predict(X_test_temp))
        print 'train_err: ' + str(train_err[i])
        print 'test_err: ' + str(test_err[i])
        print '---'

    # Plot results
    print 'plotting results'
    plt.figure()
    title = 'AP Analytics SVM(kernel = linear, with c = ' + str(c) +'): Performance x Training Set Size'
    plt.title('\n'.join(wrap(title,60)))
    plt.plot(offsets, test_err, '-', label='test error')
    plt.plot(offsets, train_err, '-', label='train error')
    plt.legend()
    plt.xlabel('Num Estimators')
    plt.ylabel('Mean Square Error')
    plt.savefig('plots/AP_Analytics/SVM/APAnalytics_linear_' + str(c) + '_PerformancexTrainingSetSize.png')
    print 'plot complete'
    ### ---

#SVM_poly
train_size = len(X_train)
offsets = range(int(0.1 * train_size), train_size, int(0.05 * train_size))
train_err = [0] * len(offsets)
test_err = [0] * len(offsets)
train_size = len(X_train)
degrees = [1, 2, 3, 5]

for d in degrees:
    for i, o in enumerate(offsets):
        print 'SVM: learning an SVM(kernel = poly) with training_set_size = ' + str(o) + ' and degree = ' + str(d)
        clf = svm.SVC(C=1, degree=d, gamma='auto', kernel='poly')
        X_train_temp = X_train[:o].copy()
        y_train_temp = y_train[:o].copy()
        X_test_temp = X_test[:o].copy()
        y_test_temp = y_test[:o].copy()
        clf.fit(X_train_temp, y_train_temp)
        train_err[i] = mean_squared_error(y_train_temp,
                                         clf.predict(X_train_temp))
        test_err[i] = mean_squared_error(y_test_temp,
                                        clf.predict(X_test_temp))
        print 'train_err: ' + str(train_err[i])
        print 'test_err: ' + str(test_err[i])
        print '---'

    # Plot results
    print 'plotting results'
    plt.figure()
    title = 'AP Analytics SVM(kernel = poly, with degree = ' + str(d) +'): Performance x Training Set Size'
    plt.title('\n'.join(wrap(title,60)))
    plt.plot(offsets, test_err, '-', label='test error')
    plt.plot(offsets, train_err, '-', label='train error')
    plt.legend()
    plt.xlabel('Num Estimators')
    plt.ylabel('Mean Square Error')
    plt.savefig('plots/AP_Analytics/SVM/APAnalytics_poly_' + str(d) + '_PerformancexTrainingSetSize.png')
    print 'plot complete'
    ### ---