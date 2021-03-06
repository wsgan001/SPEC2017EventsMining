import os
import pickle
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

class SGBRT(object):
    def __init__(self):
        self.a = None
        self.data_path = '/Users/yuxiao/Lab/projects/SPEC-CPU2017/508-name-d/namd_r_base.myt-result/'
        self.algorithm_name = 'it-95-L2-norm'

        # self.algorithm_name = 'it-95'

        # self.data_path = 'F:/linlingfeng/codes/python/perf_DATA/result/big_table'
        # self.algorithm_name = 'MinMax_TriangleCount'

    def train_sgbrt(self):
        algorithm = str(self.algorithm_name + '.csv')
        algorithm = os.path.join(self.data_path, algorithm)
        data = pd.read_csv(algorithm)

        X = data.iloc[:,1:234]
        y = data.iloc[:, 235]
        # X = X[:100]
        # y = y[:100]
        events_name = X.columns

        Err = []
        Importances = []
        Indices = []
        Events_Name = []
        Itera = 14
        for _ in range(Itera):
            print('the %s th training' % (_ + 1))
            assert len(X) == len(y)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            """ tuned """
            #forest = GradientBoostingRegressor(n_estimators=100, learning_rate=0.01, max_depth=15, random_state=0)
            """ default """
            forest = GradientBoostingRegressor()
            forest.fit(X_train, y_train)
            predicted = forest.predict(X_test)

            assert len(predicted) == len(y_test)
            y_test = np.asarray(y_test).astype(float)
            predicted = np.asarray(predicted).astype(float)
            err = np.mean(np.abs(y_test - predicted)/y_test)
            importances = forest.feature_importances_
            indices = np.argsort(importances)[::-1]

            Err.append(err)
            Indices.append(indices)
            events_Name = []
            importanceS = []
            print("Feature ranking:")
            for f in range(X.shape[1]):
                events_Name.append(events_name[indices[f]])
                importanceS.append(importances[indices[f]])
                print("%d. feature %d  %s (%f)" % (f + 1, indices[f], events_name[indices[f]], importances[indices[f]]))
            Events_Name.append(events_Name)
            Importances.append(importanceS)
            if _ < Itera-1:
                """ 每一轮训练，删除最不重要的16个事件"""
                X = pd.DataFrame(X)
                X[X.columns[indices[-16*(_+1):]]] = 0
                X = np.array(X)
            print('Error: ', err*100, '%')

        # Min_index = Err.index(min(Err))
        # for f in range(X.shape[1]):
        #     print("%d. lowest error feature %d  %s (%f)" % (f + 1, Indices[Min_index][indices[f]],
        #                                        events_name[Indices[Min_index][f]], Importances[Min_index][f]))

        res = {}
        res['result'] = [Err, Indices, Events_Name, Importances]
        output = open('result_'+self.algorithm_name+'.pkl', 'wb')
        pickle.dump(res, output)
        return res

    def build(self):
        result = self.train_sgbrt()
        print(result)
        print(result['result'][0])

if __name__ == '__main__':
    sgbrt = SGBRT()
    sgbrt.__init__()
    sgbrt.build()
