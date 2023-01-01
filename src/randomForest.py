import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from os import path
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report # for using confusion matrix
from matplotlib import pyplot as plt
import utils
import pickle
import time
import numpy as np


def test_rf():
    #Dataset: 2021-22 and 2022-23 Games - Cleaned.csv
    basepath = path.dirname(__file__)
    filename = "2021-22 and 2022-23 Games - Cleaned.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df = pd.read_csv(filepath)
    train, test = train_test_split(df,test_size = 0.2, random_state=7)
    estimators = 25
    rf = RandomForestClassifier(n_estimators=estimators)

    rf = rf.fit(train[['h_cf%']+['h_ff%']+['h_sf%']+['h_gf%']+['h_xgf%']+['h_scf%']+['h_scsf%']+['h_scgf%']+['h_scsh%']+['h_scsv%']+['h_hdsf%']+['h_hdgf%']+['h_hdsh%']+['h_hdsv%']+['h_mdsf%']+['h_mdgf%']+['h_mdsh%']+['h_mdsv%']+['h_ldsf%']+['h_ldgf%']+['h_ldsh%']+['h_ldsv%']+['h_sh%']+['h_sv%']+['h_PDO']+['a_cf%']+['a_ff%']+['a_sf%']+['a_gf%']+['a_xgf%']+['a_scf%']+['a_scsf%']+['a_scgf%']+['a_scsh%']+['a_scsv%']+['a_hdsf%']+['a_hdgf%']+['a_hdsh%']+['a_hdsv%']+['a_mdsf%']+['a_mdgf%']+['a_mdsh%']+['a_mdsv%']+['a_ldsf%']+['a_ldgf%']+['a_ldsh%']+['a_ldsv%']+['a_sh%']+['a_sv%']+['a_PDO']],train[['result']].values.ravel())
    
    predictions = rf.predict(test[['h_cf%']+['h_ff%']+['h_sf%']+['h_gf%']+['h_xgf%']+['h_scf%']+['h_scsf%']+['h_scgf%']+['h_scsh%']+['h_scsv%']+['h_hdsf%']+['h_hdgf%']+['h_hdsh%']+['h_hdsv%']+['h_mdsf%']+['h_mdgf%']+['h_mdsh%']+['h_mdsv%']+['h_ldsf%']+['h_ldgf%']+['h_ldsh%']+['h_ldsv%']+['h_sh%']+['h_sv%']+['h_PDO']+['a_cf%']+['a_ff%']+['a_sf%']+['a_gf%']+['a_xgf%']+['a_scf%']+['a_scsf%']+['a_scgf%']+['a_scsh%']+['a_scsv%']+['a_hdsf%']+['a_hdgf%']+['a_hdsh%']+['a_hdsv%']+['a_mdsf%']+['a_mdgf%']+['a_mdsh%']+['a_mdsv%']+['a_ldsf%']+['a_ldgf%']+['a_ldsh%']+['a_ldsv%']+['a_sh%']+['a_sv%']+['a_PDO']])

    accuracy = accuracy_score(test[['result']], predictions)
    print("----ACCURACY------")
    print(accuracy)

    cm = confusion_matrix(test[['result']], predictions)
    print("----CONFUSION MATRIX------")
    print(cm)

    class_report = classification_report(test[['result']], predictions, target_names=['Loss', 'Win'])
    print("----CLASSIFICATION REPORT------")
    print(class_report)


    start_time = time.time()
    importances = rf.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)
    elapsed_time = time.time() - start_time

    print(f"Elapsed time to compute the importances: {elapsed_time:.3f} seconds")

    feature_names = ['h_cf%', 'h_ff%', 'h_sf%',
       'h_gf%', 'h_xgf%', 'h_scf%', 'h_scsf%', 'h_scgf%', 'h_scsh%', 'h_scsv%',
       'h_hdsf%', 'h_hdgf%', 'h_hdsh%', 'h_hdsv%', 'h_mdsf%', 'h_mdgf%',
       'h_mdsh%', 'h_mdsv%', 'h_ldsf%', 'h_ldgf%', 'h_ldsh%', 'h_ldsv%',
       'h_sh%', 'h_sv%', 'h_PDO', 'a_cf%', 'a_ff%', 'a_sf%',
       'a_gf%', 'a_xgf%', 'a_scf%', 'a_scsf%', 'a_scgf%', 'a_scsh%', 'a_scsv%',
       'a_hdsf%', 'a_hdgf%', 'a_hdsh%', 'a_hdsv%', 'a_mdsf%', 'a_mdgf%',
       'a_mdsh%', 'a_mdsv%', 'a_ldsf%', 'a_ldgf%', 'a_ldsh%', 'a_ldsv%',
       'a_sh%', 'a_sv%', 'a_PDO']
    forest_importances = pd.Series(importances, index=feature_names)

    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
    plt.show()

    #Save model
    datum = utils.getTodaysDate(format = "%d-%m-%y",backdate = None)
    filename = 'rf_estimators' + str(estimators) + '_' + datum + '.sav'
    print(filename)
    pickle.dump(rf, open(filename, 'wb'))

test_rf()