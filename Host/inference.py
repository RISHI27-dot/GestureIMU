import pickle
import numpy as np
import pandas as pd

from pathlib import Path

from acceleration_classifier import AccelerationClassifier

def get_sign(average_array: np.ndarray, model_type: str, n_features: int):
    if len(average_array) != n_features:
        raise ValueError('Incorrect length of average array')
    
    if model_type=='knn':
        with open('./models/knn_gesture.pkl', 'rb') as f:
            model = pickle.load(f)
        res = model.predict([average_array])
    else:
        nnet = AccelerationClassifier()
        res = nnet(averaged_list=average_array)
    
    return res

def get_average(filepath: Path, model_type: str, average_window: int, n_observations: int):
    if model_type not in ['knn', 'nnet']:
        raise ValueError('Incorrect model name, choose between "knn" or "nnet"')

    df = pd.read_csv(filepath)
    df.drop(labels=['ay', 'az'], axis=1, inplace=True)
    df = (df - df.min())/(df.max()-df.min())*2-1
    if df.shape[0] < n_observations:
        #Pad data with median if the length does not match sufficient features
        add = pd.Series([np.median(df) for _ in range(n_observations-df.shape[0])])
        df = pd.concat(objs=[df['ax'], add], ignore_index=True)
    elif df.shape[0] > n_observations:
        #Truncate data to given observations if larger than required
        df = df.iloc[:n_observations, :]

    averaged_array = []
    for i in range(0, n_observations, average_window):
        average = df.iloc[i:(i+average_window)].mean()
        if type(average) is pd.Series:
            averaged_array.append(float(average.iloc[0]))
        else:
            averaged_array.append(float(average))
    
    n_features = n_observations//average_window
    gesture = get_sign(average_array=averaged_array, model_type=model_type, n_features=n_features)
    return gesture
