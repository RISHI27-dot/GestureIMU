import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier

dir = '/home/krishna/Downloads/csv'

def get_average(col: pd.Series):
    resolution = 10
    col_len = len(col)
    avg = []

    for i in range(0, col_len, resolution):
        avg.append(col.iloc[i:i+resolution].mean())
    return avg

def generate_features(dir: str, label: int):
    features = []
    target = []
    for csv in os.listdir(dir):
        l = int(csv.split('_')[0])
        if l>label:
            break

        scale = MinMaxScaler(feature_range=(-1,1))
        df = pd.read_csv(os.path.join(dir, csv))
        df = pd.DataFrame(scale.fit_transform(df))
        df.drop(labels=[1,2], inplace=True, axis=1)
        df = df.iloc[:120, :]
        ax_mean = [float(x.iloc[0]) for x in get_average(df)]
        print(ax_mean)
        features.append(ax_mean)
        target.append(l)
    
    label_csv = pd.DataFrame(features, columns=[f'x{i}' for i in range(12)] )
    label_csv['target'] = target
    label_csv.to_csv('./normalised_features.csv', index=False)

generate_features(dir, 9)

feats = pd.read_csv('./normalised_features.csv')
print(feats.isnull().sum())
feats.fillna(feats['x11'].mean(), inplace=True)
print(feats.isnull().sum())

X_train, X_val, y_train, y_val = train_test_split(feats.iloc[:,:12], feats['target'], test_size=0.25, random_state=40, shuffle=True)
clf1 = SVC(gamma='auto')
clf3 = KNeighborsClassifier()
clf1.fit(X_train, y_train)
clf3.fit(X_train, y_train)
preds1 = clf1.predict(X_val)
preds3 = clf3.predict(X_train)
print(accuracy_score(y_val, preds1))
print(accuracy_score(y_train, preds3))

# X_train, X_val, y_train, y_val = train_test_split(feats.iloc[:,:4], feats['target'], test_size=0.3, random_state=25, shuffle=True)
# clf = SVC(gamma='auto')
# clf.fit(X_train, y_train)
# preds = clf.predict(X_val)
# # accuracy_score(y_val, preds)
# print(accuracy_score(y_val, preds))

from keras.layers import Dense, Input
from keras.models import Model

inp = Input((12,))
fc1 = Dense(32, activation='relu')(inp)
fc2 = Dense(16, activation='relu')(fc1)
fc3 = Dense(10, activation='softmax')(fc2)

model = Model(inputs=inp, outputs=fc3)
model.summary()

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
hist = model.fit(
    X_train,
    y_train,
    epochs=20,
    validation_data=(X_val, y_val),
    verbose=1,
    shuffle=True
)
print("k")
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_keras_model(model)
print("hello")
tflite_model = converter.convert()
print("hello1")

with open('./gesture.tflite', 'wb') as f:
    print("hello2")
    f.write(tflite_model)