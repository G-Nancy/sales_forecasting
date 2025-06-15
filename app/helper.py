import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import datetime

def separate_closed_open_days(dataframe):
  return np.array(dataframe[dataframe['open']==0].index), np.array(dataframe[dataframe['open']!=0].index)

def flag_near_christmas(row):
    if (row['date'] >= pd.Timestamp(datetime.date(2013, 12, 14))) & (row['date'] <= pd.Timestamp(datetime.date(2013, 12, 23))):
        return 1
    elif (row['date'] >= pd.Timestamp((datetime.date(2014, 12, 14)))) & (row['date'] <= pd.Timestamp((datetime.date(2014, 12, 23)))):
        return 1
    else:
        return 0

def flag_near_easter(row):
    if (row['date'] >= pd.Timestamp(datetime.date(2013, 3, 25))) & (row['date'] <= pd.Timestamp(datetime.date(2013, 3, 29))):
        return 1
    elif (row['date'] >= pd.Timestamp(datetime.date(2014, 4, 14))) & (row['date'] <= pd.Timestamp(datetime.date(2014, 4, 18))):
        return 1
    elif (row['date'] >= pd.Timestamp(datetime.date(2015, 3, 29))) & (row['date'] <= pd.Timestamp(datetime.date(2015, 4, 3))):
        return 1
    else:
        return 0
    
def get_year(date):
    return date.year

def get_month(date):
    return date.month


def preprocess(input):
    month_avg_sales_dict = pickle.load(open('pkl_dow_avg_salespperson_dict.p','rb'))
    dow_avg_salespperson_dict = pickle.load(open('pkl_dow_avg_salespperson_dict.p','rb'))
    store_avg_sales_dict = pickle.load(open('pkl_store_avg_sales_dict.p','rb'))
    store_avg_salesperperson_dict = pickle.load(open('pkl_store_avg_salespperson_dict.p','rb'))

    X_test = pd.DataFrame(input)

    closed_days_t, open_days_t = separate_closed_open_days(X_test)
    X_test_closed = X_test.loc[closed_days_t]
    X_test_open = X_test.loc[open_days_t]
    X_test_open['dow_avg_sales/person'] = X_test_open['day_of_week'].replace(dow_avg_salespperson_dict)
    X_test_open['store_avg_sales']=X_test_open['store_ID'].replace(store_avg_sales_dict)
    X_test_open['store_avg_sales/person']=X_test_open['store_ID'].replace(store_avg_salesperperson_dict)
    X_test_open['date'] = pd.to_datetime(X_test_open['date'])

    X_test_open['nearchristmas'] = X_test_open.apply(flag_near_christmas,axis=1)
    X_test_open['neareaster'] = X_test_open.apply(flag_near_easter,axis=1)
    X_test_open['year'] = X_test_open['date'].apply(get_year)
    X_test_open['month'] = X_test_open['date'].apply(get_month)
    X_test_open = pd.concat((X_test_open,pd.get_dummies(X_test_open['year'],drop_first=True,dtype=int)),axis=1)
    X_test_open['month_avg_sales'] = X_test_open['month'].replace(month_avg_sales_dict)
    X_test_open = X_test_open.rename(columns=str)
    cols = ['nb_customers_on_day', 'promotion', 'school_holiday','dow_avg_sales/person', 'store_avg_sales', 'store_avg_sales/person','nearchristmas', 'neareaster', '2014', '2015', 'month_avg_sales']
    X_test_open = X_test_open.reindex(columns=cols, fill_value=0)

    return X_test_open, X_test_closed

def run_model(mylist):
    print(mylist)
    xgb_reg = pickle.load(open('pkl_model.p','rb'))
    
    X_new = [mylist]
    print(X_new)
    X_test_open, X_test_closed = preprocess(X_new)
    X_test_open['prediction']  = xgb_reg.predict(X_test_open)
    X_test_closed['prediction']=0
    allpreds = np.concatenate((np.array(X_test_open['prediction'] ), np.array(X_test_closed['prediction'])))
    print(allpreds)
    return allpreds
