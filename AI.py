import os.path

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


ROOTDIR = os.path.dirname(os.path.abspath(__file__))

models = {
    'logistic regression' : LogisticRegression,
    'k nearest neighbours' : KNeighborsClassifier,
    'support vector machine': SVC

}

def create_model(file_name, save = True, model_to_use= 'logistic regression'):


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
        model_name = str(file_name) + '_finalized_model.sav'
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


def check():
    print('hooray')


if __name__ == "__main__":


    #create_model(file_name=ROOTDIR + '/datasets/snap_start', model_to_use='k nearest neighbours')
    # create_model(file_name=ROOTDIR + '/datasets/snap_start', model_to_use='k nearest neighbours')
    # create_model(file_name=ROOTDIR + '/datasets/snap_start', model_to_use='k nearest neighbours')
    #create_model(file_name=ROOTDIR + '/datasets/snap_end', model_to_use='k nearest neighbours')
    #create_model(file_name=ROOTDIR + '/datasets/snapFull', model_to_use='logistic regression')


    snap_start = Gestures.Gesture(name='snap_start', func = lambda: print('snap_start'))
    snap_end = Gestures.Gesture(name='snap_end', func = lambda: print('snap_end'))
    snap = Gestures.Movement(start_ges=snap_start, end_ges=snap_end, func = lambda : print('snap'))



    print(snap_start.model, snap_end.model)

    # s = Gestures.Gesture(name= 'snapFull')
    # snap = Gestures.Movement(s, func = lambda : print('snap'))
    # print(s.model)

    import SmartController as sm
    import cv2
    import handLandmarks as hl


    cap = cv2.VideoCapture(-1)
    detector = hl.handDetector()



    controller = sm.Controller()

    home = sm.Screen(name = 'home')

    # home.add_gesture(snap_start)
    # home.add_gesture(snap_end)
    home.add_gesture(snap)

    controller.add_screen(home)





    while True:
        success, img = cap.read()

        img = cv2.flip(img,1)

        img, lmListR, lmListL, handedness = detector.get_info(img)


        cv2.imshow('img', img)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if len(lmListR)!=0 or len(lmListL)!=0:

            controller.run([],detector =detector, x=0, y=0)
