import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib


# I manually saved this values after execution
cooling_score = 0.915804311837919
heating_score = 0.830290529142604


def predict_heating(x): 
  x = np.array(x).reshape(1, -1)
  model = joblib.load(heating_lr_filename)
  return model.predict(x)[0]


def predict_cooling(x): 
  x = np.array(x).reshape(1, -1)
  model = joblib.load(cooling_lr_filename)
  return model.predict(x)[0]


def get_cooling_score():
  return cooling_score


def get_heating_score():
  return heating_score


if __name__ == "__main__":
  print('---read excel file---')
  df = pd.read_excel('./model/ENB2012_data.xlsx')

  print('---get target columns---')
  y1 = df['Y1']
  y2 = df['Y2']
  
  print('---get attribute columns---')
  X = df.drop(columns=['Y1', 'Y2'])

  print('---train-test split---')
  X1_train, X1_test, y1_train, y1_test = train_test_split(X, y1, test_size=0.3, random_state=7)
  X2_train, X2_test, y2_train, y2_test = train_test_split(X, y2, test_size=0.3, random_state=7)

  print('---create models---')
  heating_lr = LinearRegression()
  cooling_lr = LinearRegression()

  print('---fit models---')
  heating_lr.fit(X1_train.values, y1_train.values)
  cooling_lr.fit(X2_train.values, y2_train.values)


  print('---saving models---')
  heating_lr_filename = './model/heating_lr.sav'
  cooling_lr_filename = './model/cooling_lr.sav'
  joblib.dump(heating_lr, heating_lr_filename)
  joblib.dump(cooling_lr, cooling_lr_filename)

  print('---get scores from loaded models---')
  loaded_model_heating_lr = joblib.load(heating_lr_filename)
  heating_lr_score = loaded_model_heating_lr.score(X1_test.values, y1_test.values)
  loaded_model_cooling_lr = joblib.load(cooling_lr_filename)
  cooling_lr_score = loaded_model_heating_lr.score(X2_test.values, y2_test.values)
  print(heating_lr_score, cooling_lr_score)