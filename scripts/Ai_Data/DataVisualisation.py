#Data Visualisation

import pandas as pd
from matplotlib import pyplot as plt
from definitions.config import ROOTDIR
import matplotlib.pyplot as plt
import os



#load our data
gesture = 'gun'
dt = pd.read_csv(os.path.join(ROOTDIR,'datasets_old', 'datasets', gesture, gesture + '.csv'))





dt1 = dt.loc[ dt['gesture']==gesture + '_start']

Xoutliers = [42,44,43,130,131]

for o in Xoutliers:
    print(o)
    dt2 = dt1.drop(o)


#plot our data

print(dt2)
for col in dt2.columns:

    dt_points = dt2[col]

    try:
        dt_points.plot(marker = 'o')

    except Exception as e:
        print(e)

    else:
        plt.title(label=col)
        plt.show()







