import os.path
import numpy as np
import csv

import pandas as pd
import sklearn
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import pickle

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import LocalOutlierFactor

import scripts.detectors.Gestures


ROOTDIR = os.path.dirname(os.path.abspath(__file__))

models = {
    'logistic regression' : LogisticRegression,
    'k nearest neighbours' : KNeighborsClassifier,
    'support vector machine': SVC

}


def create_pipe(file_name, save=True, model_to_use='logistic regression',name='' ):
    data_file = str(file_name) + '.csv'
    data = pd.read_csv(data_file)


    # Pandas ".iloc" expects row_indexer, column_indexer
    X = data.iloc[:, :-1].values
    # Now let's tell the dataframe which column we want for the target/labels.
    y = data['gesture']

    # Test size specifies how much of the data you want to set aside for the testing set.
    # Random_state parameter is just a random seed we can use.
    # You can use it if you'd like to reproduce these specific results.
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y,
                                                                                test_size=0.20, )  # random_state=27)

    #RobustScaler(),QuantileTransformer(),KBinsDiscretizer(n_bins=5),
    pipe = make_pipeline(Normalizer(),StandardScaler(), LogisticRegression(max_iter=1000,))



    pipe.fit(X_train, y_train)



    model_prediction = pipe.predict(X_test)

    if save:
        model_name = str(file_name) + '_finalized_pipe_'+ name +'.sav'
        pickle.dump(pipe, open(model_name, 'wb'))


    print(classification_report(model_prediction, y_test))


def create_model(file_name, save = True, model_to_use= 'logistic regression',name=''):



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

    #SVC_model = sklearn.svm.SVC()
    # # KNN model requires you to specify n_neighbors,
    # # the number of points the classifier will look at to determine what class a new point belongs to
    #KNN_model = KNeighborsClassifier(n_neighbors=5)

    #l_reg_model = LogisticRegression()

    model = models[model_to_use]()




    # SVC_model.fit(X_train, y_train)
    # KNN_model.fit(X_train, y_train)
    # l_reg_model.fit(X_train, y_train)

    model.fit(X_train, y_train)


    # SVC_prediction = SVC_model.predict(X_test)
    # KNN_prediction = KNN_model.predict(X_test)
    # l_reg_prediction = l_reg_model.predict(X_test)

    model_prediction = model.predict(X_test)


    if save:
        model_name = str(file_name) + '_finalized_model' + name + '.sav'
        pickle.dump(model, open(model_name, 'wb'))


    # Accuracy score is the simplest way to evaluate
    # print(accuracy_score(SVC_prediction, y_test))
    #print(accuracy_score(KNN_prediction, y_test))
    #print(accuracy_score(l_reg_prediction, y_test))
    # But Confusion Matrix and Classification Report give more details about performance
    #print(confusion_matrix(SVC_prediction, y_test))
    #print(classification_report(KNN_prediction, y_test))
    #print(classification_report(l_reg_prediction, y_test))

    print(classification_report(model_prediction, y_test))

'''
the function takes in a model and data
and take out variuos evaluation function

vars:
    @model_file, @data_file -
                                strings file locations and name
                                
it is important to note that the scores might not be so relevant if the same data was used to create the model
'''
def model_metric(model_file,data_file, *args):



    metrics = {i:True for i in args}

    print(metrics)

    model = pickle.load(open(model_file, 'rb'))
    print(model)
    data = pd.read_csv(data_file)

    # Pandas ".iloc" expects row_indexer, column_indexer
    X = data.iloc[:,:-1].values
    # Now let's tell the dataframe which column we want for the target/labels.
    y = data['gesture']

    # Test size specifies how much of the data you want to set aside for the testing set.
    # Random_state parameter is just a random seed we can use.
    # You can use it if you'd like to reproduce these specific results.
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.20,) #random_state=27)

    model_prediction = model.predict(X_test)


    if metrics.get('accuracy'):
        print('Test Accuracy     : {:.3f}'.format(accuracy_score(y_test, model_prediction)))
        print('Training Accuracy : {:.3f}'.format(model.score(X_train, y_train)))

    if metrics.get('confusion matrix'):
        conf_mat = confusion_matrix(y_test, model_prediction)
        print(conf_mat)

    if metrics.get('classification'):
        print(classification_report(y_test, model_prediction))


    if metrics.get('log loss'):
        from sklearn.metrics import log_loss

        print('Test Log Loss   : %.3f'%log_loss(y_test, model.predict_proba(X_test)))
        print('Train Log Loss  : %.3f'%log_loss(y_train, model.predict_proba(X_train)))


    if metrics.get('missclassified') or metrics.get('zero one loss'):
        from sklearn.metrics import zero_one_loss

        print('Number of Misclassificied Examples   : ', zero_one_loss(y_test, model_prediction, normalize=False))
        print('Fraction of Misclassificied Examples : ', zero_one_loss(y_test, model_prediction))


    if metrics.get('balanced accuracy'):
        from sklearn.metrics import balanced_accuracy_score

        print('Balanced Accuracy          : ', balanced_accuracy_score(y_test, model_prediction))
        print('Balanced Accuracy Adjusted : ', balanced_accuracy_score(y_test, model_prediction, adjusted=True))


    if metrics.get('fbeta'):
        from sklearn.metrics import fbeta_score

        print('Fbeta Favouring Precision : ', fbeta_score(y_test, model_prediction, beta=0.5, average=None))
        print('Fbeta Favouring Recall    : ', fbeta_score(y_test, model_prediction, beta=2.0, average=None))


    if metrics.get('hamming'):
        from sklearn.metrics import hamming_loss

        print('Hamming Loss : ', hamming_loss(y_test, model_prediction))









def test_model(model_file, true_folder, false_folder):
    #load the model
    model = pickle.load(open(model_file, 'rb'))


    true = []
    #load true files
    for filename in os.listdir(true_folder):
        # Check if the current file is a regular file (not a directory)
        if os.path.isfile(os.path.join(true_folder, filename)):
            # Add the file name to the list
            try:
            # Add the file name to the list
                f = pd.read_csv(os.path.join(true_folder, filename))
            #f = f.iloc[:,:].values
                f = f.iloc[:, 1:].values
                pred = model.predict(f)[0]

                true.append(pred)

            except:pass
            #true.append(model.predict(np.array(data, dtype='int8')))


    false = []
    #load true files
    for filename in os.listdir(false_folder):
        # Check if the current file is a regular file (not a directory)
        if os.path.isfile(os.path.join(false_folder, filename)):

            try:
            # Add the file name to the list
                f = pd.read_csv(os.path.join(false_folder, filename))
            #f = f.iloc[:,:].values
                f = f.iloc[:, 1:].values

                pred = model.predict(f)[0]

                false.append(pred)

            except:pass



    #Tpredictions = model.predict(true)
    #Fpredictions = model.predict(false)

    print(f'false recognitions {false}')
    print(f'true recognitions {true}')



def run_tester(model_file):
    model = pickle.load(open(model_file, 'rb'))
    import cv2
    import handLandmarks as hl
    cap = cv2.VideoCapture(0)
    detector = hl.handDetector()

    ges = Gestures.Gesture(name='test')
    ges.model = model
    print(ges.model)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        img, lmListR, lmListL, handedness = detector.get_info(img)

        if len(lmListR) >0 or len(lmListL)>0:
            try:
                angles = ges.create_angle_list(detector,-1)
                result = ges.model.predict(np.array([angles]))[0]
                if result !='nope':
                    print(result)

            except Exception as e: pass#print(e)

        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            cv2.destroyAllWindows()
            break



def remove_outliers(data_file):
    from sklearn.neighbors import LocalOutlierFactor


    # Generate some sample data
    # Add the file name to the list
    X = pd.read_csv(data_file)
    # f = f.iloc[:,:].values
    X = X.iloc[0:199, 18:19].values

    import seaborn
    import matplotlib.pyplot as plt
    seaborn.scatterplot(X)
    plt.figure()
    #plt.show()
    s=seaborn.boxplot(X)

    plt.show()
    # Create the outlier detector
    detector = LocalOutlierFactor(n_neighbors=3)

    # Fit the detector and predict outliers
    outliers = detector.fit_predict(X)

    # Remove outliers from the original data
    X_clean = [X[i] for i, label in enumerate(outliers) if label != -1]

    # Print the cleaned data
    #print(X_clean)




def check():
    print('hooray')






#files we are using test drink flash
if __name__ == "__main__":

    ges = 'flash'

    file_name = os.path.join(ROOTDIR, 'datasets', ges, ges)

    remove_outliers(file_name + '.csv')

    #create_pipe(file_name, name='')

    model_file = os.path.join(ROOTDIR, 'datasets', ges, ges + '_finalized_pipe_outliers.sav')
    true_folder = os.path.join(ROOTDIR, 'datasets', 'datasets', ges, 'recognitions', 'true' )
    false_folder = os.path.join(ROOTDIR, 'datasets', 'datasets', ges, 'recognitions', 'false')


    #create_model(file_name, name='outliers')

    #run_tester(model_file)

    #test_model(model_file, true_folder, false_folder)
    #
    #model_metric(model_file,file_name+'.csv','classification')

