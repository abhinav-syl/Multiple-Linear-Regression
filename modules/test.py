from sklearn.metrics import mean_squared_error
from train_model import predict
import os
import pickle
import numpy as np
from sklearn.metrics import r2_score


class testing(predict):
    def __init__(self):
        self.files = []
        self.dir = 'data/test/'
        for path in os.listdir(self.dir):
            self.files.append(path)

    def normalize(self, df):
        for i in df.columns:
            df[i] = df[i] / max(df[i])
        df = df.fillna(0)
        return df

    def run(self):
        df = self.json_to_df()
        df = df.drop(['Pump Suction Temperature', 'Auxiliary Boilers Feed Water Header Pressure', 'Motor Voltage', 'Auxiliary Boilers A/B Feed Water Header Pressure 2'], axis=1)
        df = self.normalize(df)
        print(df)
        y_true = df['Pump Radial Bearing Vibration']
        x_test = []
        df = df.drop(['Pump Radial Bearing Vibration'], axis=1)
        for i in range(0, len(df)):
            x_test.append(df.iloc[i])
        x_test = np.array(x_test)

        y_true = np.array(y_true)
        y_true = y_true.reshape((y_true.shape[0], 1))

        model = pickle.load(open('sklearn.sav', 'rb'))
        y_pred = model.predict(x_test)
        print('RMSE = ', mean_squared_error(y_pred, y_true, squared=False))
        print('R2 Score = ', r2_score(y_true, y_pred))


testing().run()
