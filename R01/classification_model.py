from feature_extraction_training import read_and_extract, trained_model_store
from feature_generation_training import *

from sklearn import svm, linear_model, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold

import numpy as np

def model_training(model_save_directory):
    '''
    training the classification model based on the input prediction_session_index, and the trained model will be stored
    in the model_save_directory.
    :param prediction_session_index:
    :param model_save_directory:
    :return:
    '''
    platform_list = ['mindtrails_overlap', 'templeton_overlap']
    prediction_session_index = 2
    feature_vector, truth_vector, participant_list, demographic_dict, prediction_session, feature_item_list = None, None, None, None, None, None
    for platform in platform_list:
        if platform == 'mindtrails_overlap':
            feature_vector, truth_vector, participant_list, demographic_dict, prediction_session, feature_item_list = \
                classification_model_training_mindtrails_overlap(platform, prediction_session_index)
        if platform == 'templeton_overlap':
            feature_vector, truth_vector, participant_list, demographic_dict, prediction_session, feature_item_list = \
                classification_model_training_templeton_overlap(platform, prediction_session_index)

        svm_model = svm_model_training(feature_vector, truth_vector)
        trained_model_store(svm_model, model_save_directory, platform, '_SVM_training_parameter.txt')

        lr_model = logistic_regression_model_training(feature_vector, truth_vector)
        trained_model_store(lr_model, model_save_directory, platform, '_logistic_regression_training_parameter.txt')

        rf_model = random_forest_model_training(feature_vector, truth_vector)
        trained_model_store(rf_model, model_save_directory, platform, '_random_forest_training_parameter.txt')

        model_testing(platform, feature_vector, truth_vector, participant_list, prediction_session)


def classification_model_training_mindtrails_overlap(platform, prediction_session_index):
    session_list = ['PRE', 'SESSION1', 'SESSION2']

    demographic_dict, OASIS_dict, RR_dict, BBSIQ_dict, dwell_time_dict, session_completion_dict, dropout_label, \
    control_normal_dict = read_and_extract(platform)

    prediction_session = session_list[prediction_session_index]
    training_set_session = session_list[0: prediction_session_index]
    participant_list = []
    for e in dropout_label:
        if (int(e) > 419) or (int(e) < 20):
            if (e in control_normal_dict['training']) and (
                    dropout_label[e][session_list[prediction_session_index - 1]] == '0'):
                participant_list.append(e)

    feature_vector, truth_vector, feature_item_list = r01_mindtrails_feature_vector_generation(training_set_session,
                                                                                               RR_dict, BBSIQ_dict,
                                                                                               OASIS_dict,
                                                                                               demographic_dict,
                                                                                               dwell_time_dict,
                                                                                               participant_list,
                                                                                               dropout_label,
                                                                                               prediction_session)

    return feature_vector, truth_vector, participant_list, demographic_dict, prediction_session, feature_item_list


def classification_model_training_templeton_overlap(platform, prediction_session_index):
    session_list = ['preTest', 'firstSession', 'secondSession']

    credibility_dict, mental_dict, whatibelieve_dict, affect_dict, trial_dict, demographic_dict, session_completion_dict, \
    dropout_label = read_and_extract(platform)

    prediction_session = session_list[prediction_session_index]
    training_set_session = session_list[0: prediction_session_index]
    participant_list = []
    for e in dropout_label:
        if dropout_label[e][session_list[prediction_session_index - 1]] == '0':
            participant_list.append(e)

    feature_vector, truth_vector, feature_item_list = r01_templeton_feature_vector_generation(training_set_session,
                                                                                              prediction_session,
                                                                                              participant_list,
                                                                                              credibility_dict,
                                                                                              mental_dict, whatibelieve_dict,
                                                                                              affect_dict,
                                                                                              trial_dict,
                                                                                              demographic_dict,
                                                                                              session_completion_dict,
                                                                                              dropout_label)

    return feature_vector, truth_vector, participant_list, demographic_dict, prediction_session, feature_item_list


def svm_model_training(feature_vector, truth_vector):
    svm_model = svm.SVC(C=1, tol=1e-3, probability=True, gamma='scale')
    svm_model.fit(feature_vector, truth_vector)
    return svm_model


def logistic_regression_model_training(feature_vector, truth_vector):
    lr_model = linear_model.LogisticRegression()
    lr_model.fit(feature_vector, truth_vector)
    return lr_model


def random_forest_model_training(feature_vector, truth_vector):
    rf_model = RandomForestClassifier(
        n_estimators=10, criterion="gini", max_features="auto", max_depth=2, min_samples_split=2,
        min_samples_leaf=1, random_state=0, bootstrap=True, min_weight_fraction_leaf=0.0,
        n_jobs=1, oob_score=False, verbose=0, warm_start=False
    )
    rf_model.fit(feature_vector, truth_vector)
    return rf_model


def model_testing(platform, feature_vector, truth_vector, participant_list, prediction_session):

    print("========================================================")
    print('DATASET ==> ' + platform)
    print('Number of Participants for ' + prediction_session + ' ==> ' + str(len(feature_vector)))
    print('Feature Vector Dimension ==> ' + str(len(feature_vector)) + ', ' + str(len(feature_vector[0])))
    print('')

    X = range(len(feature_vector))
    kf = KFold(n_splits=10, random_state=None, shuffle=True)
    kf.get_n_splits(X)

    f1_score_svm_list, f1_score_lr_list, f1_score_rf_list = [], [], []
    precision_svm_list, precision_lr_list, precision_rf_list = [], [], []

    for train_index, test_index in kf.split(X):
        data_train, data_test, truth_train, truth_test = [], [], [], []
        participant_list_train, participant_list_test = [], []

        for i in train_index:
            data_train.append(feature_vector[i])
            truth_train.append(truth_vector[i])
            participant_list_train.append(participant_list[i])
        for i in test_index:
            data_test.append(feature_vector[i])
            truth_test.append(truth_vector[i])
            participant_list_test.append(participant_list[i])

        svm_model = svm_model_training(data_train, truth_train)
        lr_model = logistic_regression_model_training(data_train, truth_train)
        rf_model = random_forest_model_training(data_train, truth_train)

        svm_prediction = svm_model.predict(data_test)
        lr_prediction = lr_model.predict(data_test)
        rf_prediction = rf_model.predict(data_test)

        fscore_svm = metrics.f1_score(truth_test, svm_prediction, average='micro')
        fscore_lr = metrics.f1_score(truth_test, lr_prediction, average='micro')
        fscore_rf = metrics.f1_score(truth_test, rf_prediction, average='micro')

        f1_score_svm_list.append(fscore_svm)
        f1_score_lr_list.append(fscore_lr)
        f1_score_rf_list.append(fscore_rf)

        precision_svm = metrics.precision_score(truth_test, svm_prediction)
        precision_lr = metrics.precision_score(truth_test, lr_prediction)
        precision_rf = metrics.precision_score(truth_test, rf_prediction)

        precision_svm_list.append(precision_svm)
        precision_lr_list.append(precision_lr)
        precision_rf_list.append(precision_rf)

    mean_f1score_svm = np.mean(f1_score_svm_list)
    std_f1score_svm = np.std(f1_score_svm_list)
    mean_precision_svm = np.mean(precision_svm_list)

    mean_f1score_lr = np.mean(f1_score_lr_list)
    std_f1score_lr = np.std(f1_score_lr_list)
    mean_precision_lr = np.mean(precision_lr_list)

    mean_f1score_rf = np.mean(f1_score_rf_list)
    std_f1score_rf = np.std(f1_score_rf_list)
    mean_precision_rf = np.mean(precision_rf_list)

    print 'prediction_session ==>', prediction_session
    print 'SVM classifier ==>                ', 'f1 score mean', mean_f1score_svm, 'f1 score std', std_f1score_svm, 'precision', mean_precision_svm
    print 'Logisitc Regression classifier ==>', 'f1 score mean', mean_f1score_lr, 'f1 score std', std_f1score_lr, 'precision', mean_precision_lr
    print 'Random Forest classifier ==>      ', 'f1 score mean', mean_f1score_rf, 'f1 score std', std_f1score_rf, 'precision', mean_precision_rf
    print("========================================================")
    print '\n'
