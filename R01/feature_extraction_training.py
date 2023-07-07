import csv
import os
import time
import pandas as pd
import numpy as np
import cPickle as pickle

def trained_model_store(model, model_save_directory, platform, filename):
    if os.path.isdir(model_save_directory):
        saveDictFile(model, model_save_directory + platform + filename)
    else:
        os.mkdir(model_save_directory)

def trained_model_retrieve(model_save_directory, platform, filename):
    model = loadDictFile(model_save_directory + platform + filename)
    return model
def csvRead(filename):
    """
    Useful csv method
    :param filename:
    :return: csv reader object
    """
    ff = csv.reader(open(filename,'r'))
    return ff

def loadDictFile(fileName):
    if (os.path.isfile(fileName)) == True:
        f = open(fileName,'rb')
        modelDict = pickle.load(f)
        f.close()
        return modelDict
    else:
        print('load model function, file is not exist!')

def saveDictFile(dict, fileName):
    f = file(fileName,'wb')
    pickle.dump(dict,f)
    f.close()

def calibrate(missing_value,correct_value):
    if correct_value != missing_value:
        return correct_value
    else:
        #return np.NaN
        return 0

def read_and_extract(platform):
    """
    Reads through csv files and generates appropriate dictinaries
    :param platform:
    """
    task_time = None
    if platform == 'mindtrails_overlap':
        dir_path = 'data/Mindtrails_11_10_2017/'
        task_dict = {
            'PRE': ['RR', 'BBSIQ', 'OASIS', 'demographic', 'dwell_time'],
            'SESSION1': ['OASIS', 'dwell_time'],
            'SESSION2': ['OASIS', 'trial'],
        }
        task_time = dir_path + 'preprocessing/time_log_1110.csv'

        # Get dropout labels for each participant
        session_completion_dict, dropout_label = participant_session_completion_extract(platform, task_time,
                                                                                        task_dict.keys())
        demographic_dict, OASIS_dict, RR_dict, BBSIQ_dict, dwell_time_dict, control_normal_dict = \
            feature_generate_mindtrails_overlap(dir_path)

        return demographic_dict, OASIS_dict, RR_dict, BBSIQ_dict, dwell_time_dict, session_completion_dict, \
               dropout_label, control_normal_dict

    if platform == 'templeton_overlap':
        dir_path = 'data/Templeton_Oct_10_2017/'
        task_dict = {
            'preTest': ['credibility', 'demographic', 'mental', 'whatibelieve'],
            'firstSession': ['affect_pre', 'trial', 'affect_post'],
            'secondSession': ['affect_pre', 'trial', 'affect_post', 'whatibelieve'],
        }

        task_time = dir_path + 'preprocessing/time_log_1010.csv'

        # Get dropout labels for each participant
        session_completion_dict, dropout_label = participant_session_completion_extract(platform, task_time,
                                                                                        task_dict.keys())

        credibility_dict, mental_dict, whatibelieve_dict, affect_dict, trial_dict, demographics_dict = feature_generate_templeton_overlap(dir_path)

        return credibility_dict, mental_dict, whatibelieve_dict, affect_dict, trial_dict, demographics_dict, session_completion_dict, dropout_label

def participant_session_completion_extract(platform, task_time, session_name_list):
    """
    Extracts completion from task time file, and creates dropout labels
    :param platform:
    :param task_time:
    :param session_name_list:
    :return: session_completion_dict, dropout_label
    """
    # items to return
    session_completion_dict, dropout_label = {}, {}
    # read file
    ff = csvRead(task_time)
    # mindtrails
    if platform == 'mindtrails' or platform == 'mindtrails_overlap':
        for line in ff:
            if (line[0] != 'session_name') and (line[0] != 'participantdao_id'):
                if (line[1] != 'datetime_CR'):
                    id = int(line[0])
                    session_completion_dict[id] = {
                        'PRE': line[2],
                        'SESSION1': line[3],
                        'SESSION2': line[4],
                        'SESSION3': line[5],
                        'SESSION4': line[6],
                        'SESSION5': line[7],
                        'SESSION6': line[8],
                        'SESSION7': line[9],
                        'SESSION8': line[10],
                        'POST': line[1]
                    }
    # templeton
    if platform == 'templeton' or platform == 'templeton_overlap':
        for line in ff:
            if (line[0] != 'sessionName') and (line[0] != 'participantId'):
                if(line[1] != 'datetime_CR'):
                    id =int(line[0])
                    session_completion_dict[id] = {
                        'preTest': line[2],
                        'firstSession': line[3],
                        'secondSession': line[4],
                        'thridSession': line[5],
                        'fourthSession': line[6],
                    }
    # create dropout labels to be used in model testing
    for e in session_completion_dict:
        dropout_label[e] = {}
        for i in session_name_list:
            if session_completion_dict[e][i] != '':
                dropout_label[e][i] = '0'
            else:
                dropout_label[e][i] = '1'

    return session_completion_dict, dropout_label

def feature_generate_mindtrails_overlap(dir_path):
    demographic_dict, OASIS_dict, RR_dict, BBSIQ_dict, dwell_time_dict, control_normal_dict = {}, {}, {}, {}, {}, {}

    OASIS = dir_path + 'OA_label_fixed_11_10_2017.csv'
    RR = dir_path + 'RR_recovered_Nov_10_2017.csv'
    BBSIQ = dir_path + 'BBSIQ_recovered_Nov_10_2017.csv'
    demographic = dir_path + 'Demographic_recovered_Nov_10_2017.csv'
    control = dir_path + 'ParticipantExportDAO_recovered_Nov_10_2017.csv'
    test_dict = {'OASIS': OASIS, 'RR': RR, 'BBSIQ': BBSIQ, 'demographic': demographic, 'control_normal_group': control}

    for t in test_dict:
        if t == 'demographic':
            demographic_dict = mindtrails_demographic_extract(test_dict[t])
        elif t == 'OASIS':
            OASIS_dict = mindtrails_OASIS_extract(test_dict[t])
        elif t == 'RR':
            RR_dict = mindtrails_RR_extract(test_dict[t])
        elif t == 'BBSIQ':
            BBSIQ_dict = mindtrails_BBSIQ_extract(test_dict[t])
        elif t == 'control_normal_group':
            control_normal_dict = mindtrails_control_normal_group_extract(control)

    dwell_time_dict = mindtrails_dwell_time_extract(dir_path)

    return demographic_dict, OASIS_dict, RR_dict, BBSIQ_dict, dwell_time_dict, control_normal_dict

def feature_generate_templeton_overlap(dir_path):
    credibility_dict, mental_dict, whatibelieve, affect_dict, trial_dict, demographics_dict = {}, {}, {}, {}, {}, {}

    credibility = dir_path + 'Credibility_recovered_Oct_10_2017.csv'
    mental = dir_path + 'MentalHealthHistory_recovered_Oct_10_2017.csv'
    whatibelieve = dir_path + 'WhatIBelieve_recovered_Oct_10_2017.csv'
    affect = dir_path + 'Affect_recovered_Oct_10_2017.csv'
    trial = dir_path + 'JsPsychTrial_recovered_Oct_10_2017.csv'
    demographic = dir_path + 'Demographics_recovered_Oct_10_2017.csv'

    test_dict = {'affect': affect, 'credibility': credibility, 'mental': mental, 'whatibelieve': whatibelieve,
                 'trial': trial, 'demographic': demographic}

    for t in test_dict:
        if t == 'demographic':
            demographic_dict = templeton_demographic_extract(test_dict[t])
        elif t == 'affect':
            affect_dict = templeton_affect_extract(test_dict[t])
        elif t == 'credibility':
            credibility_dict = templeton_credibility_extract(test_dict[t])
        elif t == 'mental':
            mental_dict = templeton_mental_extract(test_dict[t])
        elif t == 'whatibelieve':
            whatibelieve_dict = templeton_whatibelieve_extract(test_dict[t])
        elif t == 'trial':
            trial_dict = templeton_trial_extract(test_dict[t])

    return credibility_dict, mental_dict, whatibelieve_dict, affect_dict, trial_dict, demographics_dict

##########################################################
####         feature of Mindtrails
##########################################################

def mindtrails_demographic_extract(demographic):
    ff = csvRead(demographic)

    demographic_dict = {}
    for line in ff:
        if line[9] != 'participantRSA':
            participant_id = int(line[9])
            time = line[1]
            birth_year = line[0]
            education = line[2]
            employmentStat = line[3]
            ethnicity = line[4]
            gender = line[5]
            income = line[7]
            maritalStat = line[8]
            participant_reason = line[10]
            race = line[11]
            country = line[12]

            demographic_dict[participant_id] = {
                'birth_year': birth_year,
                'country': country,
                'education': education,
                'employmentStat': employmentStat,
                'ethnicity': ethnicity,
                'gender': gender,
                'income': income,
                'maritalStat': maritalStat,
                'race': race
            }

    return demographic_dict

def mindtrails_OASIS_extract(OASIS):
    ff = csvRead(OASIS)

    OASIS_dict = {}
    for line in ff:
        if line[8] != 'participantRSA' and str.isdigit(line[8]):
            participant_id = int(line[8])
            sessionid = line[9]

            anxious_freq = calibrate(555, int(line[0]))
            anxious_sev = calibrate(555, int(line[1]))
            avoid = calibrate(555, int(line[2]))
            interfere = calibrate(555, int(line[5]))
            interfere_social = calibrate(555, int(line[6]))

            if participant_id in OASIS_dict:
                OASIS_dict[participant_id][sessionid] = {
                    'anxious_freq': anxious_freq,
                    'anxious_sev': anxious_sev,
                    'avoid': avoid,
                    'interfere': interfere,
                    'interfere_social': interfere_social
                }
            else:
                OASIS_dict[participant_id] = {
                    sessionid:{
                        'anxious_freq': anxious_freq,
                        'anxious_sev': anxious_sev,
                        'avoid': avoid,
                        'interfere': interfere,
                        'interfere_social': interfere_social
                    }
                }
    return OASIS_dict

def mindtrails_RR_extract(RR):
    ff = csvRead(RR)

    RR_dict = {}
    for line in ff:
        if line[26] != 'participantRSA' and str.isdigit(line[26]):
            participant_id = int(line[26])
            sessionid = line[31]
            time = line[4]

            blood_test_NF = calibrate(555, int(line[0]))
            blood_test_NS = calibrate(555, int(line[1]))
            blood_test_PF = calibrate(555, int(line[2]))
            blood_test_PS = calibrate(555, int(line[3]))
            elevator_NF = calibrate(555, int(line[5]))
            elevator_NS = calibrate(555, int(line[6]))
            elevator_PF = calibrate(555, int(line[7]))
            elevator_PS = calibrate(555, int(line[8]))
            job_NF = calibrate(555, int(line[10]))
            job_NS = calibrate(555, int(line[11]))
            job_PF = calibrate(555, int(line[12]))
            job_PS = calibrate(555, int(line[13]))
            lunch_NF = calibrate(555, int(line[14]))
            lunch_NS = calibrate(555, int(line[15]))
            lunch_PF = calibrate(555, int(line[16]))
            lunch_PS = calibrate(555, int(line[17]))
            meeting_friend_NF = calibrate(555, int(line[18]))
            meeting_friend_NS = calibrate(555, int(line[19]))
            meeting_friend_PF = calibrate(555, int(line[20]))
            meeting_friend_PS = calibrate(555, int(line[21]))
            noise_NF = calibrate(555, int(line[22]))
            noise_NS = calibrate(555, int(line[23]))
            noise_PF = calibrate(555, int(line[24]))
            noise_PS = calibrate(555, int(line[25]))
            scrape_NF = calibrate(555, int(line[27]))
            scrape_NS = calibrate(555, int(line[28]))
            scrape_PF = calibrate(555, int(line[29]))
            scrape_PS = calibrate(555, int(line[30]))
            shopping_NF = calibrate(555, int(line[32]))
            shopping_NS = calibrate(555, int(line[33]))
            shopping_PF = calibrate(555, int(line[34]))
            shopping_PS = calibrate(555, int(line[35]))
            wedding_NF = calibrate(555, int(line[36]))
            wedding_NS = calibrate(555, int(line[37]))
            wedding_PF = calibrate(555, int(line[38]))
            wedding_PS = calibrate(555, int(line[39]))

            if participant_id in RR_dict:
                RR_dict[participant_id][sessionid] = {
                    'blood_test_NF': blood_test_NF, 'blood_test_NS': blood_test_NS, 'blood_test_PF': blood_test_PF,
                    'blood_test_PS': blood_test_PS, 'elevator_NF': elevator_NF, 'elevator_NS': elevator_NS,
                    'elevator_PF': elevator_PF, 'elevator_PS': elevator_PS, 'job_NF': job_NF,
                    'job_NS': job_NS, 'job_PF': job_PF, 'job_PS': job_PS,
                    'lunch_NF': lunch_NF, 'lunch_NS': lunch_NS, 'lunch_PF': lunch_PF,
                    'lunch_PS': lunch_PS, 'meeting_friend_NF': meeting_friend_NF, 'meeting_friend_NS': meeting_friend_NS,
                    'meeting_friend_PF': meeting_friend_PF, 'meeting_friend_PS': meeting_friend_PS, 'noise_NF': noise_NF,
                    'noise_NS': noise_NS, 'noise_PF': noise_PF, 'noise_PS': noise_PS,
                    'scrape_NF': scrape_NF, 'scrape_NS': scrape_NS, 'scrape_PF': scrape_PF,
                    'scrape_PS': scrape_PS, 'shopping_NF': shopping_NF, 'shopping_NS': shopping_NS,
                    'shopping_PF': shopping_PF, 'shopping_PS': shopping_PS, 'wedding_NF': wedding_NF,
                    'wedding_NS': wedding_NS, 'wedding_PF': wedding_PF, 'wedding_PS': wedding_PS
                }
            else:
                RR_dict[participant_id] = {
                    sessionid: {
                        'blood_test_NF': blood_test_NF, 'blood_test_NS': blood_test_NS, 'blood_test_PF': blood_test_PF,
                        'blood_test_PS': blood_test_PS, 'elevator_NF': elevator_NF, 'elevator_NS': elevator_NS,
                        'elevator_PF': elevator_PF, 'elevator_PS': elevator_PS, 'job_NF': job_NF,
                        'job_NS': job_NS, 'job_PF': job_PF, 'job_PS': job_PS,
                        'lunch_NF': lunch_NF, 'lunch_NS': lunch_NS, 'lunch_PF': lunch_PF,
                        'lunch_PS': lunch_PS, 'meeting_friend_NF': meeting_friend_NF,
                        'meeting_friend_NS': meeting_friend_NS,
                        'meeting_friend_PF': meeting_friend_PF, 'meeting_friend_PS': meeting_friend_PS,
                        'noise_NF': noise_NF,
                        'noise_NS': noise_NS, 'noise_PF': noise_PF, 'noise_PS': noise_PS,
                        'scrape_NF': scrape_NF, 'scrape_NS': scrape_NS, 'scrape_PF': scrape_PF,
                        'scrape_PS': scrape_PS, 'shopping_NF': shopping_NF, 'shopping_NS': shopping_NS,
                        'shopping_PF': shopping_PF, 'shopping_PS': shopping_PS, 'wedding_NF': wedding_NF,
                        'wedding_NS': wedding_NS, 'wedding_PF': wedding_PF, 'wedding_PS': wedding_PS
                    }
                }


    return RR_dict

def mindtrails_BBSIQ_extract(BBSIQ):
    ff = csvRead(BBSIQ)

    BBSIQ_dict = {}
    for line in ff:
        if line[26] != 'participantRSA' and str.isdigit(line[26]):
            participant_id = int(line[26])
            time = line[9]
            sessionid = line[30]

            breath_flu = calibrate(555, int(line[0]))
            breath_physically = calibrate(555, int(line[1]))
            breath_suffocate = calibrate(555, int(line[2]))
            chest_heart = calibrate(555, int(line[3]))
            chest_indigestion = calibrate(555, int(line[4]))
            chest_sore = calibrate(555, int(line[5]))
            confused_cold = calibrate(555, int(line[6]))
            confused_outofmind = calibrate(555, int(line[7]))
            confused_work = calibrate(555, int(line[8]))
            dizzy_ate = calibrate(555, int(line[10]))
            dizzy_ill = calibrate(555, int(line[11]))
            dizzy_overtired = calibrate(555, int(line[12]))
            friend_helpful = calibrate(555, int(line[13]))
            friend_incompetent = calibrate(555, int(line[14]))
            friend_moreoften = calibrate(555, int(line[15]))
            heart_active = calibrate(555, int(line[16]))
            heart_excited = calibrate(555, int(line[17]))
            heart_wrong = calibrate(555, int(line[18]))
            jolt_burglar = calibrate(555, int(line[20]))
            jolt_dream = calibrate(555, int(line[21]))
            jolt_wind = calibrate(555, int(line[22]))
            lightheaded_eat = calibrate(555, int(line[23]))
            lightheaded_faint = calibrate(555, int(line[24]))
            lightheaded_sleep = calibrate(555, int(line[25]))
            party_boring = calibrate(555, int(line[27]))
            party_hear = calibrate(555, int(line[28]))
            party_preoccupied = calibrate(555, int(line[29]))
            shop_bored = calibrate(555, int(line[31]))
            hop_concentrating = calibrate(555, int(line[32]))
            shop_irritating = calibrate(555, int(line[33]))
            smoke_cig = calibrate(555, int(line[34]))
            smoke_food = calibrate(555, int(line[35]))
            smoke_house = calibrate(555, int(line[36]))
            urgent_bill = calibrate(555, int(line[37]))
            urgent_died = calibrate(555, int(line[38]))
            urgent_junk = calibrate(555, int(line[39]))
            vision_glasses = calibrate(555, int(line[40]))
            vision_illness = calibrate(555, int(line[41]))
            vision_strained = calibrate(555, int(line[42]))
            visitors_bored = calibrate(555, int(line[43]))
            visitors_engagement = calibrate(555, int(line[44]))
            visitors_outstay = calibrate(555, int(line[45]))

            if participant_id in BBSIQ_dict:
                BBSIQ_dict[participant_id][sessionid] = {
                    'breath_flu': breath_flu, 'breath_physically': breath_physically, 'breath_suffocate': breath_suffocate,
                    'chest_heart': chest_heart, 'chest_indigestion': chest_indigestion, 'chest_sore': chest_sore,
                    'confused_cold': confused_cold, 'confused_outofmind': confused_outofmind, 'confused_work': confused_work,
                    'dizzy_ate': dizzy_ate, 'dizzy_ill': dizzy_ill, 'dizzy_overtired': dizzy_overtired,
                    'friend_helpful': friend_helpful, 'friend_incompetent': friend_incompetent,
                    'friend_moreoften': friend_moreoften,
                    'heart_active': heart_active, 'heart_excited': heart_excited, 'heart_wrong': heart_wrong,
                    'jolt_burglar': jolt_burglar, 'jolt_dream': jolt_dream, 'jolt_wind': jolt_wind,
                    'lightheaded_eat': lightheaded_eat, 'lightheaded_faint': lightheaded_faint,
                    'lightheaded_sleep': lightheaded_sleep,
                    'party_boring': party_boring, 'party_hear': party_hear, 'party_preoccupied': party_preoccupied,
                    'shop_bored': shop_bored, 'hop_concentrating': hop_concentrating, 'shop_irritating': shop_irritating,
                    'smoke_cig': smoke_cig, 'smoke_food': smoke_food, 'smoke_house': smoke_house,
                    'urgent_bill': urgent_bill, 'urgent_died': urgent_died, 'urgent_junk': urgent_junk,
                    'vision_glasses': vision_glasses, 'vision_illness': vision_illness, 'vision_strained': vision_strained,
                    'visitors_bored': visitors_bored, 'visitors_engagement': visitors_engagement,
                    'visitors_outstay': visitors_outstay
                }
            else:
                BBSIQ_dict[participant_id] = {
                    sessionid: {
                        'breath_flu': breath_flu, 'breath_physically': breath_physically,
                        'breath_suffocate': breath_suffocate,
                        'chest_heart': chest_heart, 'chest_indigestion': chest_indigestion, 'chest_sore': chest_sore,
                        'confused_cold': confused_cold, 'confused_outofmind': confused_outofmind,
                        'confused_work': confused_work,
                        'dizzy_ate': dizzy_ate, 'dizzy_ill': dizzy_ill, 'dizzy_overtired': dizzy_overtired,
                        'friend_helpful': friend_helpful, 'friend_incompetent': friend_incompetent,
                        'friend_moreoften': friend_moreoften,
                        'heart_active': heart_active, 'heart_excited': heart_excited, 'heart_wrong': heart_wrong,
                        'jolt_burglar': jolt_burglar, 'jolt_dream': jolt_dream, 'jolt_wind': jolt_wind,
                        'lightheaded_eat': lightheaded_eat, 'lightheaded_faint': lightheaded_faint,
                        'lightheaded_sleep': lightheaded_sleep,
                        'party_boring': party_boring, 'party_hear': party_hear, 'party_preoccupied': party_preoccupied,
                        'shop_bored': shop_bored, 'hop_concentrating': hop_concentrating,
                        'shop_irritating': shop_irritating,
                        'smoke_cig': smoke_cig, 'smoke_food': smoke_food, 'smoke_house': smoke_house,
                        'urgent_bill': urgent_bill, 'urgent_died': urgent_died, 'urgent_junk': urgent_junk,
                        'vision_glasses': vision_glasses, 'vision_illness': vision_illness,
                        'vision_strained': vision_strained,
                        'visitors_bored': visitors_bored, 'visitors_engagement': visitors_engagement,
                        'visitors_outstay': visitors_outstay
                    }
                }
    return BBSIQ_dict

def mindtrails_dwell_time_extract(dir_path):
    task_time_dict = loadDictFile(dir_path + 'preprocessing/task_time_dict.txt')
    dwell_time_dict = {}
    duration_two_task = []
    for participant_id in task_time_dict:
        # print e, task_dict[e]
        dwell_time_dict[int(participant_id)] = {}
        for session_id in task_time_dict[participant_id]:
            dwell_time_dict[int(participant_id)][session_id] = {}
            if len(task_time_dict[participant_id][session_id]) == 1:
                dwell_time_dict[int(participant_id)][session_id]['DURATION'] = 0
            else:
                t_list = []

                for k in task_time_dict[participant_id][session_id]:
                    t = task_time_dict[participant_id][session_id][k] #time e.g. 2017-09-26 17:41:08
                    ts = time.mktime(time.strptime(str(pd.to_datetime(t)), '%Y-%m-%d %H:%M:%S'))
                    t_list.append(ts)
                    dwell_time_dict[int(participant_id)][session_id][k] = ts
                dur = max(t_list) - min(t_list)
                dwell_time_dict[int(participant_id)][session_id]['DURATION'] = dur

                t_list_sort = sorted(t_list)
                for i in range(0, len(t_list_sort) - 1):
                    duration_two_task.append(t_list_sort[i + 1] - t_list_sort[i])

    # print(dwell_time_dict)
    return dwell_time_dict

def mindtrails_control_normal_group_extract(control):
    no_training = []
    training = []
    ff = csvRead(control)
    for line in ff:
        if line[0] != 'active':
            id = int(line[5])
            control_flag = line[2]
            if (control_flag == 'NEUTRAL') and ((id in no_training) is False):
                no_training.append(id)
            elif ((id in training) is False):
                training.append(id)
        control_normal_dict = {'no_training': no_training, 'training': training}

    return control_normal_dict

##########################################################
####         feature of Templeton
##########################################################

def templeton_demographic_extract(demographic):
    ff = csvRead(demographic)

    demographic_dict = {}
    for line in ff:
        participant_id = line[11]

        if participant_id != 'participantRSA':
            participant_id = int(participant_id)
            timeonpage = float(line[17])

            birth_year = int(line[0])
            country = line[1]
            device = line[3]
            education = line[4]
            employmentStat = line[5]
            ethnicity = line[6]
            gender = line[7]
            income = line[9]
            maritalStat = line[10]
            race = line[14]

            demographic_dict[participant_id] = {
                'timeonpage': timeonpage,
                'birth_year': birth_year,
                'country': country,
                'device': device,
                'education': education,
                'employmentStat': employmentStat,
                'ethnicity': ethnicity,
                'gender': gender,
                'income': income,
                'maritalStat': maritalStat,
                'race': race
            }
    return demographic_dict


def templeton_affect_extract(affect):
    ff = csvRead(affect)

    affect_dict = {}
    for line in ff:
        participant_id = line[3]
        sessionid = line[5]
        tag = line[6]

        if participant_id != 'participantRSA':
            participant_id = int(participant_id)
            timeonpage = float(line[7])
            negFeelings = calibrate(555,int(line[2]))
            posFeelings = calibrate(555,int(line[4]))

            if participant_id in affect_dict:
                if sessionid in affect_dict[participant_id]:
                    affect_dict[participant_id][sessionid][tag] = {
                        'negFeelings': negFeelings,
                        'posFeelings': posFeelings,
                        'timeonpage': timeonpage
                    }
                else:
                    affect_dict[participant_id][sessionid] = {
                        tag: {
                            'negFeelings': negFeelings,
                            'posFeelings': posFeelings,
                            'timeonpage': timeonpage
                        }
                    }

            else:
                affect_dict[participant_id] = {
                    sessionid: {
                        tag: {
                            'negFeelings': negFeelings,
                            'posFeelings': posFeelings,
                            'timeonpage': timeonpage
                        }
                    }
                }

    return affect_dict


def templeton_credibility_extract(credibility):
    ff = csvRead(credibility)

    credibility_dict = {}
    for line in ff:
        participant_id = line[5]
        if participant_id != 'participantRSA':
            participant_id = int(participant_id)
            timeonpage = float(line[8])

            if participant_id in credibility_dict:
                credibility_dict[participant_id]['preTest'] = {'timeonpage': timeonpage}
            else:
                credibility_dict[participant_id] = {
                    'preTest': {
                        'timeonpage': timeonpage
                    }
                }
    return credibility_dict


def templeton_mental_extract(mental):
    ff = csvRead(mental)

    mental_dict = {}
    for line in ff:
        participant_id = line[32]

        if participant_id != 'participantRSA':
            participant_id = int(participant_id)
            timeonpage = float(line[49])

            if participant_id in mental_dict:
                mental_dict[participant_id]['preTest'] = {'timeonpage': timeonpage}
            else:
                mental_dict[participant_id] = {
                    'preTest': {
                        'timeonpage': timeonpage
                    }
                }
    return mental_dict


def templeton_whatibelieve_extract(whatibelieve):
    ff = csvRead(whatibelieve)

    whatibelieve_dict = {}
    for line in ff:
        participant_id = line[7]
        sessionid = line[10]

        if participant_id != 'participantRSA':
            participant_id = int(participant_id)
            timeonpage = float(line[12])

            alwaysChangeThinking = calibrate(555,int(line[0]))
            compared = calibrate(555,int(line[1]))
            difficultTasks = calibrate(555,int(line[3]))
            hardlyEver = calibrate(555,int(line[4]))
            learn = calibrate(555,int(line[6]))
            particularThinking = calibrate(555,int(line[8]))
            performEffectively = calibrate(555,int(line[9]))
            wrongWill = calibrate(555,int(line[13]))

            ####### Scoring of three different subscales ########
            NGSES = np.nanmean(np.array([difficultTasks,compared,performEffectively])) * 3
            GMM = np.nanmean(np.array([5-learn,particularThinking,alwaysChangeThinking])) * 3
            Optimism = np.nanmean(np.array([hardlyEver,wrongWill])) * 2


            if participant_id in whatibelieve_dict:
                whatibelieve_dict[participant_id][sessionid] = {
                    'alwaysChangeThinking': alwaysChangeThinking,
                    'compared': compared,
                    'difficultTasks': difficultTasks,
                    'hardlyEver': hardlyEver,
                    'learn': learn,
                    'particularThinking':particularThinking,
                    'performEffectively': performEffectively,
                    'wrongWill': wrongWill,
                    'timeonpage': timeonpage,
                    'NGSES': NGSES,
                    'GMM': GMM,
                    'Optimism': Optimism
                }
            else:
                whatibelieve_dict[participant_id] = {}
                whatibelieve_dict[participant_id][sessionid] = {
                    'alwaysChangeThinking': alwaysChangeThinking,
                    'compared': compared,
                    'difficultTasks': difficultTasks,
                    'hardlyEver': hardlyEver,
                    'learn': learn,
                    'particularThinking': particularThinking,
                    'performEffectively': performEffectively,
                    'wrongWill': wrongWill,
                    'timeonpage': timeonpage,
                    'NGSES': NGSES,
                    'GMM': GMM,
                    'Optimism': Optimism
                }
    return whatibelieve_dict

def templeton_trial_extract(trial):
    ##########################################################################################
    # 1. rt: react time of
    # 2. rt_correct: react time of first attempt
    # 3. time_elapsed: accumulate time of rt
    # 4. unit: millisecond
    ##########################################################################################

    ff = csvRead(trial)

    enroll_condition = {}
    trial_dict = {}
    for line in ff:
        participant_id = line[6]
        sessionid = line[9]
        condition = line[1]

        first_try_correct = line[2]
        device = line[3]

        if participant_id != 'participantId':
            participant_id = int(participant_id)
            time_elapsed = float(line[12])

            if (participant_id in enroll_condition) is False:
                enroll_condition[participant_id] = condition

            if participant_id in trial_dict:
                if sessionid in trial_dict[participant_id]:
                    trial_dict[participant_id][sessionid]['time_elapsed'].append(time_elapsed)
                    trial_dict[participant_id][sessionid]['first_try_correct'].append(first_try_correct)

                else:
                    trial_dict[participant_id][sessionid] = {
                        'time_elapsed': [time_elapsed],
                        'device': device,
                        'first_try_correct': [first_try_correct]
                    }
            else:
                trial_dict[participant_id] = {
                    sessionid:
                    {
                    'time_elapsed': [time_elapsed],
                    'device': device,
                    'first_try_correct': [first_try_correct]
                    }
                }

    return trial_dict
