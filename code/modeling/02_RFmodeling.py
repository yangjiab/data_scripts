import os
import sys
import yaml
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np
import pymannkendall as mk


def simulate_dynamic_trajectory(df_data, model, features_list):    
    trajectory = df_data.copy()
    n = len(trajectory)
    trajectory['WB_pred'] = np.nan
    trajectory.loc[:1, 'WB_pred'] = trajectory.loc[:1, 'WaterBarr']
    for t in range(2, n):
        feature_vec = []
        for col in features_list:
            if col == 'WB_lag1':
                lag1_val = trajectory.loc[t-1, 'WB_pred'] if not np.isnan(trajectory.loc[t-1, 'WB_pred']) else trajectory.loc[t-1, 'WaterBarr']
                feature_vec.append(lag1_val)
            elif col == 'WB_lag2':
                feature_vec.append(trajectory.loc[t-2, 'WB_pred'] if not np.isnan(trajectory.loc[t-2, 'WB_pred']) else trajectory.loc[t-2, 'WaterBarr'])
            elif col == 'prec_lag1':
                feature_vec.append(trajectory.loc[t-1, 'prec'] if not np.isnan(trajectory.loc[t-1, 'prec']) else trajectory.loc[t-1, 'prec'])
            elif col == 'prec_lag2':
                feature_vec.append(trajectory.loc[t-2, 'prec'] if not np.isnan(trajectory.loc[t-2, 'prec']) else trajectory.loc[t-2, 'prec'])
            elif col == 'pet_lag1':
                feature_vec.append(trajectory.loc[t-1, 'pet'] if not np.isnan(trajectory.loc[t-1, 'pet']) else trajectory.loc[t-1, 'pet'])
            elif col == 'pet_lag2':
                feature_vec.append(trajectory.loc[t-2, 'pet'] if not np.isnan(trajectory.loc[t-2, 'pet']) else trajectory.loc[t-2, 'pet'])
            else:
                feature_vec.append(trajectory.loc[t, col])
        
        X_t = np.array([feature_vec])
        model_pred = model.predict(X_t)[0]
        waterbarr_pred = lag1_val + model_pred
        trajectory.loc[t, 'WB_pred'] = waterbarr_pred
    
    return trajectory['WB_pred'].values


