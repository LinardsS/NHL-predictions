import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from os import path
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report # for using confusion matrix
from matplotlib import pyplot as plt
import utils
import pickle

def test_dt():
    #Dataset: 2021-22 and 2022-23 Games - Cleaned.csv
    basepath = path.dirname(__file__)
    filename = "2021-22 and 2022-23 Games - Cleaned.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df = pd.read_csv(filepath)
    train, test = train_test_split(df,test_size = 0.2, random_state=7)
    clf = DecisionTreeClassifier(ccp_alpha = 0.01)
    clf = clf.fit(train[['h_cf%']+['h_ff%']+['h_sf%']+['h_gf%']+['h_xgf%']+['h_scf%']+['h_scsf%']+['h_scgf%']+['h_scsh%']+['h_scsv%']+['h_hdsf%']+['h_hdgf%']+['h_hdsh%']+['h_hdsv%']+['h_mdsf%']+['h_mdgf%']+['h_mdsh%']+['h_mdsv%']+['h_ldsf%']+['h_ldgf%']+['h_ldsh%']+['h_ldsv%']+['h_sh%']+['h_sv%']+['h_PDO']+['a_cf%']+['a_ff%']+['a_sf%']+['a_gf%']+['a_xgf%']+['a_scf%']+['a_scsf%']+['a_scgf%']+['a_scsh%']+['a_scsv%']+['a_hdsf%']+['a_hdgf%']+['a_hdsh%']+['a_hdsv%']+['a_mdsf%']+['a_mdgf%']+['a_mdsh%']+['a_mdsv%']+['a_ldsf%']+['a_ldgf%']+['a_ldsh%']+['a_ldsv%']+['a_sh%']+['a_sv%']+['a_PDO']],train[['result']].values.ravel())
    
    predictions = clf.predict(test[['h_cf%']+['h_ff%']+['h_sf%']+['h_gf%']+['h_xgf%']+['h_scf%']+['h_scsf%']+['h_scgf%']+['h_scsh%']+['h_scsv%']+['h_hdsf%']+['h_hdgf%']+['h_hdsh%']+['h_hdsv%']+['h_mdsf%']+['h_mdgf%']+['h_mdsh%']+['h_mdsv%']+['h_ldsf%']+['h_ldgf%']+['h_ldsh%']+['h_ldsv%']+['h_sh%']+['h_sv%']+['h_PDO']+['a_cf%']+['a_ff%']+['a_sf%']+['a_gf%']+['a_xgf%']+['a_scf%']+['a_scsf%']+['a_scgf%']+['a_scsh%']+['a_scsv%']+['a_hdsf%']+['a_hdgf%']+['a_hdsh%']+['a_hdsv%']+['a_mdsf%']+['a_mdgf%']+['a_mdsh%']+['a_mdsv%']+['a_ldsf%']+['a_ldgf%']+['a_ldsh%']+['a_ldsv%']+['a_sh%']+['a_sv%']+['a_PDO']])

    accuracy = accuracy_score(test[['result']], predictions)
    print("----ACCURACY------")
    print(accuracy)

    cm = confusion_matrix(test[['result']], predictions)
    print("----CONFUSION MATRIX------")
    print(cm)

    class_report = classification_report(test[['result']], predictions, target_names=['Loss', 'Win'])
    print("----CLASSIFICATION REPORT------")
    print(class_report)
    
    feature_names = ['h_cf%', 'h_ff%', 'h_sf%',
       'h_gf%', 'h_xgf%', 'h_scf%', 'h_scsf%', 'h_scgf%', 'h_scsh%', 'h_scsv%',
       'h_hdsf%', 'h_hdgf%', 'h_hdsh%', 'h_hdsv%', 'h_mdsf%', 'h_mdgf%',
       'h_mdsh%', 'h_mdsv%', 'h_ldsf%', 'h_ldgf%', 'h_ldsh%', 'h_ldsv%',
       'h_sh%', 'h_sv%', 'h_PDO', 'a_cf%', 'a_ff%', 'a_sf%',
       'a_gf%', 'a_xgf%', 'a_scf%', 'a_scsf%', 'a_scgf%', 'a_scsh%', 'a_scsv%',
       'a_hdsf%', 'a_hdgf%', 'a_hdsh%', 'a_hdsv%', 'a_mdsf%', 'a_mdgf%',
       'a_mdsh%', 'a_mdsv%', 'a_ldsf%', 'a_ldgf%', 'a_ldsh%', 'a_ldsv%',
       'a_sh%', 'a_sv%', 'a_PDO']
    feature_importance = pd.DataFrame(clf.feature_importances_, index = feature_names)

    # plot the feature importance
    feature_plot = feature_importance.plot(kind='bar')
    #feature_plot.show()

    #plot the tree itself
    fig = plt.figure(figsize=(25,20))
    tree_plot = plot_tree(clf,
                  feature_names = feature_names,
                  class_names={0:'Loss', 1:'Win'},
                  filled = True,
                  fontsize = 12)
    plt.show()

    #Save model
    datum = utils.getTodaysDate(format = "%d-%m-%y",backdate = None)
    filename = 'dt_' + datum + '.sav'
    pickle.dump(clf, open(filename, 'wb'))
test_dt()