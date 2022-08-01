import json
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import os
import pickle


class predict:
    def __init__(self):
        # get  a list of json files in train folder
        self.files = []
        self.dir = 'data/test/'
        for path in os.listdir(self.dir):
            self.files.append(path)

    def to_json(self, name, operation, lists):
        with open(name, operation) as infile:
            if operation == "r":
                lists = json.load(infile)
                return lists
            else:
                json_object = json.dumps(lists)
                infile.write(json_object)
                del json_object

    def json_to_df(self):
        # convert all json files into a single dataframe for further calculations
        data = []
        data_total = {}
        for file in self.files:
            data = self.to_json(self.dir + file, "r", data)
            names = []
            names = [x['name'] for x in data if x['name'] not in names]
            names = list(set(names))
            data_c = [[x['name'], x['data']] for x in data]
            for i in data_c:
                for j in i[1]:
                    try:
                        data_total[i[0]]
                    except Exception as E:
                        print(E)
                        data_total[i[0]] = []
                    data_total[i[0]].append(j['value'])
        data_comp = data_total
        df = pd.DataFrame(data=data_comp)
        df = df.fillna(0)
        return df

    def normalize(self, df):
        for i in list(df.columns):
            df[i] = df[i] / max(df[i])
        df = df.fillna(0)
        return df

    def run(self):
        df = self.json_to_df()
        df = df.drop(['Pump Suction Temperature', 'Auxiliary Boilers Feed Water Header Pressure', 'Motor Voltage', 'Auxiliary Boilers A/B Feed Water Header Pressure 2'], axis=1)
        df = self.normalize(df)
        y_true = df['Pump Radial Bearing Vibration']
        x_train = []
        df = df.drop(['Pump Radial Bearing Vibration'], axis=1)
        for i in range(0, len(df)):
            x_train.append(df.iloc[i])
        # convert to array for faster calculations
        x_train = np.array(x_train)

        y_true = np.array(y_true)
        y_true = y_true.reshape((y_true.shape[0], 1))

        model = LinearRegression().fit(x_train, y_true)

        # save the model as a pickle file
        filename = 'sklearn.sav'
        pickle.dump(model, open(filename, 'wb'))


predict().run()
