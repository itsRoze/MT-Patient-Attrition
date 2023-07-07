import datetime
import time
from _mysql import IntegrityError

import numpy as np
import MySQLdb
import json


from feature_generation import R01_credibility_extract, R01_BBSIQ_extract, R01_demographics_extract, R01_trial_extract, \
    R01_mental_extract, R01_OASIS_extract, R01_RR_extract, R01_affect_extract, R01_training_extract, \
    feature_vector_r01_overlap_with_mindtrails, feature_vector_r01_overlap_with_templeton

from feature_extraction_training import trained_model_retrieve


def predictions_for_all(secret, VERSION, model_save_directory):
    '''
        This will select all participants that are currently active who's current
         condition is 'TRAINING'.  After prediction. all participants with this
        condition should be converted to either LR_TRAINING, HR_COACH, or HR_NO_COACH'
        and we of course wholly ignore the NONE and CONTROL conditions
    '''

    creds = open(secret)
    text = creds.read()
    d = json.loads(str(text))
    creds.close()

    # Grab the version from the version file.
    version = ""

    with open(VERSION, 'r') as myfile:
        version = myfile.read().replace('\n', '')
    version = version.strip()

    R01_database_host = d['R01_database_host']
    port_number = d['port_number']
    username = d['username']
    password = d['password']
    db_name = d['db_name']

    # connect the R01 database
    R01_db = MySQLdb.connect(host=R01_database_host, port=port_number, user=username, passwd=password, db=db_name,
                             charset='utf8')

    cursor = R01_db.cursor()
    sql = "select participant.id from participant  left join study on participant.study_id = study.id " \
          "where participant.active = true and study.conditioning = \"TRAINING\""

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
    except:
        print "Error: unable to find any participants to process."
    for row in results:
        id = row[0]
        try:
            result = r01_prediction(cursor, id, model_save_directory, version)
            prediction_result_save_to_db(cursor, id, result, version)
            R01_db.commit()
            print("Saved prediction, " + str(result) + ", for participant " + str(id))
        except Exception as error:
            print("FAILED: Processing user #%s.  %s.  %s" % (id, error.__class__.__name__, error.message))
    R01_db.close()


def fetchTableForP(cursor, participantId, tableName):
    # extract data of participantId from tables
    cursor.execute("SELECT * FROM %s WHERE participant_id=%s" % (tableName, participantId))
    result = cursor.fetchall()
    if(len(result) < 1): raise Exception("No values available for Participant #%s in table %s" % (participantId, tableName))
    return result


def r01_prediction(cursor, participantId, model_save_directory, version):

    # extract data of participantId from tables
    affect_dict = R01_affect_extract(fetchTableForP(cursor, participantId, "affect"))[participantId]
    BBSIQ_dict = R01_BBSIQ_extract(fetchTableForP(cursor, participantId, "bbsiq"))[participantId]
    credibility_dict = R01_credibility_extract(fetchTableForP(cursor, participantId, "credibility"))[participantId]
    demographics_dict = R01_demographics_extract(fetchTableForP(cursor, participantId, "demographics"))[participantId]
    trial_dict = R01_trial_extract(fetchTableForP(cursor, participantId, "js_psych_trial"))[participantId]
    mental_dict = R01_mental_extract(fetchTableForP(cursor, participantId, "mental_health_history"))[participantId]
    OASIS_dict = R01_OASIS_extract(fetchTableForP(cursor, participantId, "oa"))[participantId]
    RR_dict = R01_RR_extract(fetchTableForP(cursor, participantId, "rr"))[participantId]

    # check that the user has completed all requirements for questionnaires
    task_dict = {
        'preTest': ['RR', 'BBSIQ', 'OASIS', 'credibility', 'mental'],
        'firstSession': ['OASIS', 'affect']
    }
    for session in task_dict:
        for questionnaire in task_dict[session]:
            if questionnaire == 'RR' and session not in RR_dict:
                raise Exception("No values available for Participant #%s for questionnaire %s in session %s" % (participantId, questionnaire, session))
            elif questionnaire == 'BBSIQ' and session not in BBSIQ_dict:
                raise Exception("No values available for Participant #%s for questionnaire %s in session %s" % (participantId, questionnaire, session))
            elif questionnaire == 'OASIS' and session not in OASIS_dict:
                raise Exception("No values available for Participant #%s for questionnaire %s in session %s" % (participantId, questionnaire, session))
            elif questionnaire == 'credibility' and session not in credibility_dict:
                raise Exception("No values available for Participant #%s for questionnaire %s in session %s" % (participantId, questionnaire, session))
            elif questionnaire == 'mental' and session not in mental_dict:
                raise Exception("No values available for Participant #%s for questionnaire %s in session %s" % (participantId, questionnaire, session))
            elif questionnaire == 'affect' and session not in affect_dict:
                raise Exception("No values available for Participant #%s for questionnaire %s in session %s" % (participantId, questionnaire, session))

    questionnaire_list = {'preTest': ['demographics', 'mental_health_history', 'anxiety_identity', 'oa', 'anxiety_triggers', 'bbsiq', 'comorbid', 'wellness', 'mechanisms'],
                          'firstSession': ['affect', 'angular_training', 'cc', 'oa', 'return_intention']}
    # generate timeOnPage dict
    timeOnPage_dict = {}
    for sessionId in questionnaire_list:
        timeOnPage_dict[sessionId] = {}
        for item in questionnaire_list[sessionId]:
            if item == 'affect':
                cursor.execute("SELECT 'tag', 'time_on_page' FROM %s WHERE participant_id=%s AND session='%s'" % (
                item,participantId, sessionId))

                result = cursor.fetchall()
                for line in result:

                    tag = line[1]
                    timeOnPage_dict[sessionId][item + '_' + tag] = line[1]
                
            else:
                cursor.execute("SELECT time_on_page FROM %s WHERE participant_id=%s AND session='%s'" % (
                item, participantId, sessionId))

                result = cursor.fetchall()
                for line in result:
                    timeOnPage_dict[sessionId][item] = line[0]

    # # generate feature vector overlapping with mindtrails or templeton
    templeton_vector, templeton_feature_item_list = feature_vector_r01_overlap_with_templeton(credibility_dict, mental_dict, affect_dict,
                                                                 trial_dict, demographics_dict)
    mindtrails_vector, mindtrails_feature_item_list = feature_vector_r01_overlap_with_mindtrails(RR_dict, BBSIQ_dict, OASIS_dict,
                                                                 demographics_dict, timeOnPage_dict)


    # retrieve trained classification models
    rf_model_mindtrails = trained_model_retrieve(model_save_directory, 'mindtrails_overlap',
                                                 '_random_forest_training_parameter.txt')
    rf_model_templeton = trained_model_retrieve(model_save_directory, 'templeton_overlap',
                                                '_random_forest_training_parameter.txt')


    # compute predicted values of participantId
    rf_mindtrails_prediction = rf_model_mindtrails.predict_proba([mindtrails_vector])[0][1]

    rf_templeton_prediction = rf_model_templeton.predict_proba([templeton_vector])[0][1]

    prediction_value_list = []

    # prediction_value_list.append(rf_mindtrails_prediction)
    prediction_value_list.append(rf_templeton_prediction)

    return np.mean(prediction_value_list)


def prediction_result_save_to_db(cursor, participantId, result, version):
    #save result
    try :
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO attrition_prediction (participant_id, confidence, date_created, version) VALUES (%s, %s, %s, %s)"
        values = (participantId, result, timestamp, version)
        cursor.execute(sql, values)
    except IntegrityError:
        print("participant #%i already has a prediction." % participantId)

if __name__ == "__main__":
    secret = 'creds.secret'
    version = 'VERSION'
    model_save_directory = 'trained_model/'
    predictions_for_all(secret, version, model_save_directory)
