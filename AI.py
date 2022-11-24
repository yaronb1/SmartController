import pandas as pd
import sklearn
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import pickle

import Gestures



def create_model(file_name, save = True):
    data_file = str(file_name) + '.csv'
    data = pd.read_csv(data_file)

    # It is a good idea to check and make sure the data is loaded as expected.

    #print(data.head(5))

    # Pandas ".iloc" expects row_indexer, column_indexer
    X = data.iloc[:,:-1].values
    # Now let's tell the dataframe which column we want for the target/labels.
    y = data['gesture']

    # Test size specifies how much of the data you want to set aside for the testing set.
    # Random_state parameter is just a random seed we can use.
    # You can use it if you'd like to reproduce these specific results.
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.20,) #random_state=27)

    #print(X_train)
    #print(y_train)

    # SVC_model = sklearn.svm.SVC()
    # # KNN model requires you to specify n_neighbors,
    # # the number of points the classifier will look at to determine what class a new point belongs to
    # KNN_model = KNeighborsClassifier(n_neighbors=5)

    l_reg_model = LogisticRegression()




    # SVC_model.fit(X_train, y_train)
    # KNN_model.fit(X_train, y_train)
    l_reg_model.fit(X_train, y_train)


    # SVC_prediction = SVC_model.predict(X_test)
    # KNN_prediction = KNN_model.predict(X_test)
    l_reg_prediction = l_reg_model.predict(X_test)


    if save:
        model_name = str(file_name) + '_finalized_model.sav'
        pickle.dump(l_reg_model, open(model_name, 'wb'))

    # Accuracy score is the simplest way to evaluate
    # print(accuracy_score(SVC_prediction, y_test))
    # print(accuracy_score(KNN_prediction, y_test))
    print(accuracy_score(l_reg_prediction, y_test))
    # But Confusion Matrix and Classification Report give more details about performance
    #print(confusion_matrix(SVC_prediction, y_test))
    #print(classification_report(KNN_prediction, y_test))
    print(classification_report(l_reg_prediction, y_test))



def check():
    print('hooray')


path = '/home/yaron/PycharmProjects/SmartController/datasets/'
g= 'gun'

file = path + g

if __name__ == "__main__":


    #gun = Gestures.Gesture(name='gun',func=check)

    #gun.model.predict()

    create_model(file,save = False)