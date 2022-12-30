import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os import path
from sklearn.linear_model import LogisticRegression
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix # for using confusion matrix
import statsmodels.api as sm
import pickle
import utils

def test():
    logreg = LogisticRegression(max_iter = 500)
    #Dataset: 2021-22 and 2022-23 Games - Cleaned.csv
    basepath = path.dirname(__file__)
    filename = "2021-22 and 2022-23 Games - Cleaned.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df = pd.read_csv(filepath)
    #print(list(df.columns.values))
    train, test = train_test_split(df,test_size = 0.2, random_state=7) # 80%/20% training/test split
    logreg.fit(train[['h_cf%']+['h_ff%']+['h_sf%']+['h_gf%']+['h_xgf%']+['h_scf%']+['h_scsf%']+['h_scgf%']+['h_scsh%']+['h_scsv%']+['h_hdsf%']+['h_hdgf%']+['h_hdsh%']+['h_hdsv%']+['h_mdsf%']+['h_mdgf%']+['h_mdsh%']+['h_mdsv%']+['h_ldsf%']+['h_ldgf%']+['h_ldsh%']+['h_ldsv%']+['h_sh%']+['h_sv%']+['h_PDO']+['a_cf%']+['a_ff%']+['a_sf%']+['a_gf%']+['a_xgf%']+['a_scf%']+['a_scsf%']+['a_scgf%']+['a_scsh%']+['a_scsv%']+['a_hdsf%']+['a_hdgf%']+['a_hdsh%']+['a_hdsv%']+['a_mdsf%']+['a_mdgf%']+['a_mdsh%']+['a_mdsv%']+['a_ldsf%']+['a_ldgf%']+['a_ldsh%']+['a_ldsv%']+['a_sh%']+['a_sv%']+['a_PDO']],train[['result']].values.ravel())
    predict1 = logreg.predict(test[['h_cf%']+['h_ff%']+['h_sf%']+['h_gf%']+['h_xgf%']+['h_scf%']+['h_scsf%']+['h_scgf%']+['h_scsh%']+['h_scsv%']+['h_hdsf%']+['h_hdgf%']+['h_hdsh%']+['h_hdsv%']+['h_mdsf%']+['h_mdgf%']+['h_mdsh%']+['h_mdsv%']+['h_ldsf%']+['h_ldgf%']+['h_ldsh%']+['h_ldsv%']+['h_sh%']+['h_sv%']+['h_PDO']+['a_cf%']+['a_ff%']+['a_sf%']+['a_gf%']+['a_xgf%']+['a_scf%']+['a_scsf%']+['a_scgf%']+['a_scsh%']+['a_scsv%']+['a_hdsf%']+['a_hdgf%']+['a_hdsh%']+['a_hdsv%']+['a_mdsf%']+['a_mdgf%']+['a_mdsh%']+['a_mdsv%']+['a_ldsf%']+['a_ldgf%']+['a_ldsh%']+['a_ldsv%']+['a_sh%']+['a_sv%']+['a_PDO']])
    # logreg.fit(df[["h_point%"]+['a_point%']],df[['result']])
    # predict1 = logreg.predict(df[["h_point%"]+['a_point%']])
    print(predict1)
    cm1 = confusion_matrix(test[['result']],predict1)
    print(cm1)
    total1=sum(sum(cm1))
    print(total1)
    #####from confusion matrix calculate accuracy
    accuracy1=(cm1[0,0]+cm1[1,1])/total1
    print(accuracy1)
    #What are the most impacting variables?
    #### From summary of the model
    logit1=sm.Logit(df['result'],df[['h_cf%']+['h_ff%']+['h_sf%']+['h_gf%']+['h_xgf%']+['h_scf%']+['h_scsf%']+['h_scgf%']+['h_scsh%']+['h_scsv%']+['h_hdsf%']+['h_hdgf%']+['h_hdsh%']+['h_hdsv%']+['h_mdsf%']+['h_mdgf%']+['h_mdsh%']+['h_mdsv%']+['h_ldsf%']+['h_ldgf%']+['h_ldsh%']+['h_ldsv%']+['h_sh%']+['h_sv%']+['h_PDO']+['a_cf%']+['a_ff%']+['a_sf%']+['a_gf%']+['a_xgf%']+['a_scf%']+['a_scsf%']+['a_scgf%']+['a_scsh%']+['a_scsv%']+['a_hdsf%']+['a_hdgf%']+['a_hdsh%']+['a_hdsv%']+['a_mdsf%']+['a_mdgf%']+['a_mdsh%']+['a_mdsv%']+['a_ldsf%']+['a_ldgf%']+['a_ldsh%']+['a_ldsv%']+['a_sh%']+['a_sv%']+['a_PDO']])

    result1=logit1.fit()
    print(result1.summary())

    print(result1.summary2())
    
    #Save model
    datum = utils.getTodaysDate(format = "%d-%m-%y",backdate = None)
    filename = 'log_reg_NO_POINT_PERCENTAGE_' + datum + '.sav'
    pickle.dump(logreg, open(filename, 'wb'))
def loadModel(model_name):
    filename = model_name + ".sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model
# model = loadModel("log_reg_12-12-22_2")
# prediction = model.predict()
#test()