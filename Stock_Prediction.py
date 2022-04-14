# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 00:43:46 2022

@author: baskar
"""

import warnings
warnings.filterwarnings('ignore')
#Data Manipulation and Treatment
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta


#Plotting and Visualizations
import matplotlib.pyplot as plt
import seaborn as sns
#!pip install plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#Scikit-Learn for Modeling
from sklearn.metrics import mean_squared_error,r2_score, mean_absolute_error,mean_squared_log_error
#Statistics
import statsmodels.api as sm
from statsmodels.tsa.api import Holt,SimpleExpSmoothing,ExponentialSmoothing
from pmdarima import auto_arima

#Scikit-Learn for Modeling
from sklearn.metrics import mean_squared_error,r2_score, mean_absolute_error,mean_squared_log_error
#df = pd.read_csv('stock_data_x.csv', sep=",")
#df = pd.read_csv('C:/Users/baska/Downloads/NUS/Big Data/Projects/stock_data_y.csv').dropna()

l_0 = df.iloc[0].T
df_0 = l_0.to_frame()
df_0.columns = ["Day_0"]
df_fmt_0 = df_0.reset_index().rename(columns={'index':'Symbol'})
df_f0 = df_fmt_0.iloc[1: , :]
df.head()
df['Date'] =  pd.to_datetime(df.Date,format='%d/%m/%Y')
#print(type('Date'))
df.index = df['Date']
df = df.drop('Date',axis=1)
df.head()
#print(type('Date'))
model_train=df.iloc[:int(df.shape[0]*0.80)]
valid=df.iloc[int(df.shape[0]*0.80):]
y_pred=valid.copy()
model_scores_r2=[]
model_scores_mse=[]
model_scores_rmse=[]
model_scores_mae=[]
model_scores_rmsle=[]
pred_arima=[]
model_pred = []
i = 1
ARIMA_model_new_dte=[]
for d in range(1,180):
    ARIMA_model_new_dte.append(df.index[-1] + timedelta(days=d))
    model_predictions_dte=pd.DataFrame(zip(ARIMA_model_new_dte),columns=(["Date"]))          
m = model_predictions_dte
for i in range(len(df.columns)):
     tickerSymbol = df.columns[i]
     print(tickerSymbol)
     model_arima = auto_arima(model_train[tickerSymbol],trace=False, error_action='ignore', start_p=1,start_q=1,max_p=3,max_q=3,
              suppress_warnings=True,stepwise=False,seasonal=False)
     model_arima.fit(model_train[tickerSymbol])
     prediction_arima = model_arima.predict(len(valid))
     y_pred["ARIMA Model Prediction"] = prediction_arima
   
     r2_arima= r2_score(y_pred[tickerSymbol],y_pred["ARIMA Model Prediction"])
     mse_arima= mean_squared_error(y_pred[tickerSymbol],y_pred["ARIMA Model Prediction"])
     rmse_arima=np.sqrt(mean_squared_error(y_pred[tickerSymbol],y_pred["ARIMA Model Prediction"]))
     mae_arima=mean_absolute_error(y_pred[tickerSymbol],y_pred["ARIMA Model Prediction"])
     rmsle_arima = np.sqrt(mean_squared_log_error(y_pred[tickerSymbol],y_pred["ARIMA Model Prediction"]))
     model_scores_r2.append(r2_arima)
     model_scores_mse.append(mse_arima)
     model_scores_rmse.append(rmse_arima)
     model_scores_mae.append(mae_arima)
     model_scores_rmsle.append(rmsle_arima)

     ARIMA_model_new_date=[]
     ARIMA_model_new_prediction=[]

     for j in range(1,180):
         ARIMA_model_new_date.append(df.index[-1] + timedelta(days=j))
         ARIMA_model_new_prediction.append(model_arima.predict(len(valid)+j)[-1])
         pd.set_option('display.float_format', lambda x: '%.6f' % x)
         model_predictions=pd.DataFrame(zip(ARIMA_model_new_prediction),columns=([tickerSymbol]))   
         model_predictions_date=pd.DataFrame(zip(ARIMA_model_new_date),columns=(["Date"])) 
         x = pd.concat([model_predictions_date,model_predictions],axis=1)         
     m = pd.merge(m,x,left_on="Date",right_on="Date")
     Predicted = m.to_csv('C:/Users/baska/Downloads/NUS/Big Data/Projects/pred_data.csv',encoding='utf-8')
     # Write the Predicted Stock Price to S3 
     s3 = boto3.resource('s3',aws_access_key_id='AKIA2I4L5O2NZ532672T', aws_secret_access_key='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')
     bucket = s3.Bucket('bsaw-client-info','Predicted')
     result = object.put(Body=Predicted)
# Get 30 days Predicted Price        
l_30 = m.iloc[30].T
df_30 = l_30.to_frame()
df_30.columns = ["Day_30"]
df_30_fmt = df_30.reset_index().rename(columns={'index':'Symbol'})
df_f30 = df_30_fmt.iloc[1: , :].drop('Symbol', 1)
df_0_30 = pd.concat([df_f0,df_f30],axis=1)         
# Get 60 days Predicted Price        
l_60 = m.iloc[60].T
df_60 = l_60.to_frame()
df_60.columns = ["Day_60"]
df_60_fmt = df_60.reset_index().rename(columns={'index':'Symbol'})
df_f60 = df_60_fmt.iloc[1: , :].drop('Symbol', 1)
df_0_30_60 = pd.concat([df_0_30,df_f60,],axis=1)
# Get 90 days Predicted Price        
l_90 = m.iloc[90].T
df_90 = l_90.to_frame()
df_90.columns = ["Day_90"]
df_90_fmt = df_90.reset_index().rename(columns={'index':'Symbol'})
df_f90 = df_90_fmt.iloc[1: , :].drop('Symbol', 1)
df_0_30_60_90 = pd.concat([df_0_30_60,df_f90,],axis=1)
# Get 120 days Predicted Price        
l_120 = m.iloc[120].T
df_120 = l_120.to_frame()
df_120.columns = ["Day_120"]
df_120_fmt = df_120.reset_index().rename(columns={'index':'Symbol'})
df_f120 = df_120_fmt.iloc[1: , :].drop('Symbol', 1)
df_0_30_60_90_120 = pd.concat([df_0_30_60_90,df_f120,],axis=1)
# Get 180 days Predicted Price        
l_180 = m.iloc[178].T
df_180 = l_180.to_frame()
df_180.columns = ["Day_180"]
df_180_fmt = df_180.reset_index().rename(columns={'index':'Symbol'})
df_f180 = df_180_fmt.iloc[1: , :].drop('Symbol', 1)
df_final = pd.concat([df_0_30_60_90_120,df_f180,],axis=1)

# Transform as UP and Down Trend
df_final["Trend_30"] = (np.where(df_final['Day_0'] < df_final['Day_30'], "Up", "Down"))
df_final["Trend_90"] = (np.where(df_final['Day_0'] < df_final['Day_90'], "Up", "Down"))
df_final["Trend_180"] = (np.where(df_final['Day_0'] < df_final['Day_180'], "Up", "Down"))

# Transform as Volatility
df_final["Trend_V_30"] = (df_final['Day_30'] - df_final['Day_0'])/(df_final['Day_0']) * 100
df_final["Trend_V_90"] = (df_final['Day_30'] - df_final['Day_0'])/(df_final['Day_0']) * 100
df_final["Trend_V_180"] = (df_final['Day_180'] - df_final['Day_0'])/(df_final['Day_0']) * 100
Trend = df_final

#df_final.to_csv('C:/Users/baska/Downloads/NUS/Big Data/Projects/final_data.csv',encoding='utf-8',index=False)
# Write the Predicted Trend Stock Price to S3 
s3 = boto3.resource('s3',aws_access_key_id='AKIA2I4L5O2NZ532672T', aws_secret_access_key='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')
bucket = s3.Bucket('bsaw-client-info','Trend')
result = object.put(Body=Trend)
