import os.path
import numpy as np


import pandas as pd
import sklearn
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LinearRegression
import pickle


from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import Normalizer


from matplotlib import pyplot as plt


from definitions.config import ROOTDIR

models = {
    'logistic regression' : LogisticRegression,
    'k nearest neighbours' : KNeighborsClassifier,
    'support vector machine': SVC

}


def create_pipe(data, save=True, model_to_use='logistic regression',name='' ):
    # data_file = str(file_name) + '.csv'
    # data = pd.read_csv(data_file)


    # Pandas ".iloc" expects row_indexer, column_indexer
    X = data.iloc[:, :-1].values
    # Now let's tell the dataframe which column we want for the target/labels.
    y = data['gesture']

    # Test size specifies how much of the data you want to set aside for the testing set.
    # Random_state parameter is just a random seed we can use.
    # You can use it if you'd like to reproduce these specific results.
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y,
                                                                                test_size=0.20, )  # random_state=27)



    weights = {

        'nope':0.1,
        name+'_start':1,
        name+'_end':1,
    }



    #RobustScaler(),QuantileTransformer(),KBinsDiscretizer(n_bins=5),
    pipe = make_pipeline(Normalizer(),StandardScaler(), LogisticRegression(max_iter=1000,class_weight=weights))



    pipe.fit(X_train, y_train)



    model_prediction = pipe.predict(X_test)

    if save:
        model_name = os.path.join(ROOTDIR,'datasets',name,name+'_finalized_pipe_.sav')
        #model_name = str(file_name) + '_finalized_pipe_'+ name +'.sav'
        pickle.dump(pipe, open(model_name, 'wb'))

    else: return pipe


    print(classification_report(model_prediction, y_test))


def create_model(data, save = True, model_to_use= 'logistic regression',name=''):



    # data_file = str(file_name) + '.csv'
    # data = pd.read_csv(data_file)



    # It is a good idea to check and make sure the data is loaded as expected.

    #print(data.head(5))

    # Pandas ".iloc" expects row_indexer, column_indexer
    X = data.iloc[:,:-1]
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
        #model_name = str(file_name) + '_finalized_model' + name + '.sav'
        model_name = os.path.join(ROOTDIR, 'datasets', name, '_finalized_model_.sav')
        pickle.dump(model, open(model_name, 'wb'))
    else: return model


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







#the function is designed to test a model that has been altered
# we will put into various data that has been collected
#the functions takes data that has been collected(NOT THE DATA USED TO CREATE THE MODEL)
# that is eperated into true recog and false recogs.
# the true recogs must stay the same and false recogs must be seen as false t
#this will show if the altered model is better or worse than the original one

def test_model(model, true_folder, false_folder):
    #load the model
    #model = pickle.load(open(model_file, 'rb'))


    true = {}
    #load true files
    for filename in os.listdir(true_folder):
        # Check if the current file is a regular file (not a directory)
        if os.path.isfile(os.path.join(true_folder, filename)):
            # Add the file name to the list
            try:
            # Add the file name to the list
                f = pd.read_csv(os.path.join(true_folder, filename))
                print(f)
            #f = f.iloc[:,:].values
                #f = f.iloc[:, 1:].values
                pred = model.predict(f)[0]

                #true.append(pred)
                true[filename]= pred

            except Exception as e: print(e)
            #true.append(model.predict(np.array(data, dtype='int8')))


    false = {}
    #load true files
    for filename in os.listdir(false_folder):
        # Check if the current file is a regular file (not a directory)
        if os.path.isfile(os.path.join(false_folder, filename)):

            try:
            # Add the file name to the list
                f = pd.read_csv(os.path.join(false_folder, filename))
            #f = f.iloc[:,:].values
                #f = f.iloc[:, 1:].values

                pred = model.predict(f)[0]

                #false.append(pred)
                false[filename]=pred

            except Exception as e: print(e)

    return false, true


    print(f'false recognitions {false}')
    print(f'true recognitions {true}')





# pass dataframe and a list of outliers
#return dt with the list remove
#if no outliers gets passed the ufnc will remove based on the mean value
def remove_outliers(dt,outliers=[],gesture='flash_start'):


    if len(outliers)!=0:
        for o in outliers:
            dt = dt.drop(o)

        return dt

    else:
        for col in dt.columns:
            if col=='gesture':
                pass
            else:
                print(f'mean of {col} = {dt[col].mean()}')

                dt1 = dt.loc[dt['gesture'] == gesture]
                for val in dt1[col].values:
                    print(val-dt1[col].mean())

                break





#creates graph of the dataset, showing the given gesture

#when using line - gesture = 'ges'_start or 'ges'_end or nope
#when using scatter ges = 'gesture'
def visualise(dt,gesture,graph_type = 'line', ):



    #

    if graph_type=='line':

        dt1 = dt.loc[dt['gesture'] == gesture]
        for col in dt1.columns:

            dt_points = dt1[col]

            try:
                dt_points.plot(marker='o')

            except Exception as e:
                print(e)

            else:
                plt.title(label=col)
                plt.show()

    elif graph_type=='scatter':
        import seaborn

        for col in dt.columns:
            dt_points = dt[col]
            try:
                seaborn.scatterplot(dt_points.loc[dt['gesture']=='nope'])
                seaborn.scatterplot(dt_points.loc[dt['gesture'] == gesture +'_start'])
                seaborn.scatterplot(dt_points.loc[dt['gesture'] == gesture + '_end'])
            except Exception as e: print(e)
            else:
                plt.title(label=col)
                plt.show()



def check():
    print('hooray')



#this function takes the dates from the screenshots folder and sorts the recognition folder

def sort_folders(ges_name):

    import shutil
    root = os.path.join(ROOTDIR,'datasets_old','datasets')


    true_screenshots = os.listdir(os.path.join(root,'screenshots',ges_name,'true'))
    false_screenshots = os.listdir(os.path.join(root, 'screenshots', ges_name, 'false'))

    true_dates = [i[:11] for i in true_screenshots]
    false_dates = [i[:11] for i in false_screenshots]

    for file in os.listdir(os.path.join(root,ges_name,'recognitions')):
        alt_file = file.replace('-', '_')
        print(alt_file[:11])
        if alt_file[:11] in true_dates:
            shutil.move(os.path.join(root,ges_name,'recognitions',file),
                        os.path.join(root,ges_name,'recognitions','true'))
            print(f'{file} moved to true')

        elif alt_file[:11] in false_dates:
            shutil.move(os.path.join(root,ges_name,'recognitions',file),
                        os.path.join(root,ges_name,'recognitions','false'))

            print(f'{file} moved to false')



#after saving data in an incorrect format i have written this func which chanf=ges that format into a proper dataframe
#note that this func will DELETE the contents of the folder iyou provide but will use those conent to creat new files
#must provide true folder or false folder
#the wrong format was [  '[X.XXXX', 'XXXXX' ....... 'XXXXXX]' ]
# the reuired format dataframe with the headers for columns, one index and float in each column
def create_dataframe_from_wrong_format(folder):

    headers = ['thumb 1-2', 'thumb 2-3', 'thumb 3-4', 'thumb_fore 4-5', 'fore 5-6', 'fore 6-7', 'fore 7-8',
                       'fore_middle 8-9', 'middle 9-10', 'middle 10-11', 'middle 11-12', 'middle_ring 12-13',
                       'ring 13 -14',
                       'ring 14-15', 'ring 15-16', 'ring_pinky 16-17', 'pinky 17-18', 'pinky 18-19', 'pinky 19-20',
                       ]

    import csv



    for file in os.listdir(folder):
        vals = []
        dt = pd.read_csv(os.path.join(folder,file))
        print(f'file name {file}')
        # #print(dt.columns[1])
        for id,col in enumerate(dt.columns):
            if id ==0:
                col = col[1:]

            elif id ==len(dt.columns)-1:
                col = col[:-1]


            try:vals.append(float(col))
            except: vals.append(float(col[:-2]))
        print(vals)


        with open(os.path.join(folder,file), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow(vals)

#files we are using test drink flash
if __name__ == "__main__":

    ges = 'gun2'


    #create_model(file_name, name='outliers')

    #run_tester(model_file)

    #test_model(model_file, true_folder, false_folder)
    #
    #model_metric(model_file,file_name+'.csv','classification')

    file = os.path.join(ROOTDIR,'datasets',ges,ges+'.csv')
    dt = pd.read_csv(file)

    visualise(dt,gesture=ges, graph_type='scatter')


    # outliers_end = [400,527,528,529,530,531,532,586,587,589,588,493,495,482]
    # outliers_end.append([ior i in range(423, 430)])
    # outliers_end.append([i for i in range(454, 461)])
    #
    # #remove_outliers(dt)
    #
    # outliers = [22,23,24,69,0,15,56,19,20,21,25,1,2,3,4,5,6,7,16,170,60,67]
    # outliers.append([i for i in range(142,149)])
    # outliers.append([i for i in range(190,194)])
    # outliers.append([i for i in range(159, 169)])
    # outliers.append([i for i in range(61, 66)])
    #
    # #
    #dt_new = remove_outliers(dt,outliers_end)

    #dt_new = remove_outliers(dt,outliers)
    # #
    # # print(dt_new)
    # #
    #visualise(dt_new, 'flash_end')
    #

    # model = create_pipe(dt,save=False, name=ges)
    #
    # # # #
    # # # #
    # model_file = os.path.join(ROOTDIR,'datasets_old','datasets',ges, ges+'_finalized_model.sav' )
    # true_folder = os.path.join(ROOTDIR,'datasets_old','datasets',ges, 'recognitions', 'true')
    # false_folder = os.path.join(ROOTDIR, 'datasets_old', 'datasets', ges, 'recognitions', 'false')
    # #
    # # # create_dataframe_from_wrong_format(true_folder)
    # # # create_dataframe_from_wrong_format(false_folder)
    # #
    # # # # #
    # # #model = pickle.load(open(model_file, 'rb'))
    # # # #
    # false, true = test_model(model,true_folder,false_folder)
    #
    # print(f'false -  {false.values()}')
    # print(f'true - {true.values()}')




