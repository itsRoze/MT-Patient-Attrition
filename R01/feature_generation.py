from __future__ import division
import numpy as np

def calibrate(missing_value,correct_value):
    if correct_value != missing_value:
        return correct_value
    else:
        return 0

##########################################################
####         feature of R01
##########################################################
def R01_affect_extract(affect_result):
    affect_dict = {}
    for line in affect_result:
        sessionid = line[2]
        tag = line[3]
        timeonpage = float(line[4])
        # negFeelings = calibrate(555, int(line[5])) # does not exist
        posFeelings = calibrate(555, int(line[5])) 
        negFeelings = posFeelings # CHANGE THIS
        participant_id = int(line[6])

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


def R01_BBSIQ_extract(BBSIQ_result):
    BBSIQ_dict = {}
    for line in BBSIQ_result:
        sessionid = line[2]
        timeonpage = float(line[4])
        participant_id = int(line[47])

        breath_flu = calibrate(555, int(line[5]))
        breath_physically = calibrate(555, int(line[6]))
        breath_suffocate = calibrate(555, int(line[7]))
        chest_heart = calibrate(555, int(line[8]))
        chest_indigestion = calibrate(555, int(line[9]))
        chest_sore = calibrate(555, int(line[10]))
        confused_cold = calibrate(555, int(line[11]))
        confused_outofmind = calibrate(555, int(line[12]))
        confused_work = calibrate(555, int(line[13]))
        dizzy_ate = calibrate(555, int(line[14]))
        dizzy_ill = calibrate(555, int(line[15]))
        dizzy_overtired = calibrate(555, int(line[16]))
        friend_helpful = calibrate(555, int(line[17]))
        friend_incompetent = calibrate(555, int(line[18]))
        friend_moreoften = calibrate(555, int(line[19]))
        heart_active = calibrate(555, int(line[20]))
        heart_excited = calibrate(555, int(line[21]))
        heart_wrong = calibrate(555, int(line[22]))
        jolt_burglar = calibrate(555, int(line[23]))
        jolt_dream = calibrate(555, int(line[24]))
        jolt_wind = calibrate(555, int(line[25]))
        lightheaded_eat = calibrate(555, int(line[26]))
        lightheaded_faint = calibrate(555, int(line[27]))
        lightheaded_sleep = calibrate(555, int(line[28]))
        party_boring = calibrate(555, int(line[29]))
        party_hear = calibrate(555, int(line[30]))
        party_preoccupied = calibrate(555, int(line[31]))
        shop_bored = calibrate(555, int(line[32]))
        hop_concentrating = calibrate(555, int(line[33]))
        shop_irritating = calibrate(555, int(line[34]))
        smoke_cig = calibrate(555, int(line[35]))
        smoke_food = calibrate(555, int(line[36]))
        smoke_house = calibrate(555, int(line[37]))
        urgent_bill = calibrate(555, int(line[38]))
        urgent_died = calibrate(555, int(line[39]))
        urgent_junk = calibrate(555, int(line[40]))
        vision_glasses = calibrate(555, int(line[41]))
        vision_illness = calibrate(555, int(line[42]))
        vision_strained = calibrate(555, int(line[43]))
        visitors_bored = calibrate(555, int(line[44]))
        visitors_engagement = calibrate(555, int(line[45]))
        visitors_outstay = calibrate(555, int(line[46]))

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
                'visitors_outstay': visitors_outstay, 'timeonpage': timeonpage
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
                    'visitors_outstay': visitors_outstay, 'timeonpage': timeonpage
                }
            }
    return BBSIQ_dict


def R01_demographics_extract(demographics_result):
    demographics_dict = {}
    for line in demographics_result:
        participant_id = int(line[15])
        timeonpage = float(line[4])
        sessionid = line[2]
        birth_year = int(line[5])
        country = line[6]
        education = line[7]
        employmentStat = line[8]
        ethnicity = line[9]
        gender = line[10]
        income = line[11]
        maritalStat = line[12]
        # race = line[15]
        race = ethnicity # CHANGE THIS

        demographics_dict[participant_id] = {
            'timeonpage': timeonpage,
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
    return demographics_dict


def R01_OASIS_extract(OASIS_result):
    OASIS_dict = {}
    for line in OASIS_result:
        participant_id = int(line[10])
        sessionid = line[2]
        timeonpage = float(line[4])

        anxious_freq = calibrate(555, int(line[5]))
        anxious_sev = calibrate(555, int(line[6]))
        avoid = calibrate(555, int(line[7]))
        interfere = calibrate(555, int(line[8]))
        interfere_social = calibrate(555, int(line[9]))

        if participant_id in OASIS_dict:
            OASIS_dict[participant_id][sessionid] = {
                'anxious_freq': anxious_freq,
                'anxious_sev': anxious_sev,
                'avoid': avoid,
                'interfere': interfere,
                'interfere_social': interfere_social,
                'timeonpage': timeonpage
            }
        else:
            OASIS_dict[participant_id] = {
                sessionid:{
                    'anxious_freq': anxious_freq,
                    'anxious_sev': anxious_sev,
                    'avoid': avoid,
                    'interfere': interfere,
                    'interfere_social': interfere_social,
                    'timeonpage': timeonpage
                }
            }
    return OASIS_dict


def R01_RR_extract(RR_result):
    RR_dict = {}
    for line in RR_result:

        participant_id = int(line[41])
        sessionid = line[2]
        timeonpage = float(line[4])

        blood_test_NF = calibrate(555, int(line[5]))
        blood_test_NS = calibrate(555, int(line[6]))
        blood_test_PF = calibrate(555, int(line[7]))
        blood_test_PS = calibrate(555, int(line[8]))
        elevator_NF = calibrate(555, int(line[9]))
        elevator_NS = calibrate(555, int(line[10]))
        elevator_PF = calibrate(555, int(line[11]))
        elevator_PS = calibrate(555, int(line[12]))
        job_NF = calibrate(555, int(line[13]))
        job_NS = calibrate(555, int(line[14]))
        job_PF = calibrate(555, int(line[15]))
        job_PS = calibrate(555, int(line[16]))
        lunch_NF = calibrate(555, int(line[17]))
        lunch_NS = calibrate(555, int(line[18]))
        lunch_PF = calibrate(555, int(line[19]))
        lunch_PS = calibrate(555, int(line[20]))
        meeting_friend_NF = calibrate(555, int(line[21]))
        meeting_friend_NS = calibrate(555, int(line[22]))
        meeting_friend_PF = calibrate(555, int(line[23]))
        meeting_friend_PS = calibrate(555, int(line[24]))
        noise_NF = calibrate(555, int(line[25]))
        noise_NS = calibrate(555, int(line[26]))
        noise_PF = calibrate(555, int(line[27]))
        noise_PS = calibrate(555, int(line[28]))
        scrape_NF = calibrate(555, int(line[29]))
        scrape_NS = calibrate(555, int(line[30]))
        scrape_PF = calibrate(555, int(line[31]))
        scrape_PS = calibrate(555, int(line[32]))
        shopping_NF = calibrate(555, int(line[33]))
        shopping_NS = calibrate(555, int(line[34]))
        shopping_PF = calibrate(555, int(line[35]))
        shopping_PS = calibrate(555, int(line[36]))
        wedding_NF = calibrate(555, int(line[37]))
        wedding_NS = calibrate(555, int(line[38]))
        wedding_PF = calibrate(555, int(line[39]))
        wedding_PS = calibrate(555, int(line[40]))

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
                'wedding_NS': wedding_NS, 'wedding_PF': wedding_PF, 'wedding_PS': wedding_PS,
                'timeonpage': timeonpage
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
                    'wedding_NS': wedding_NS, 'wedding_PF': wedding_PF, 'wedding_PS': wedding_PS,
                    'timeonpage': timeonpage
                }
            }


    return RR_dict


def R01_credibility_extract(credibility_result):
    credibility_dict = {}
    for line in credibility_result:
        sessionid = line[2]
        timeonpage = float(line[4])
        participant_id = int(line[7])

        if participant_id in credibility_dict:
            credibility_dict[participant_id][sessionid] = {'timeonpage': timeonpage}
        else:
            credibility_dict[participant_id] = {
                sessionid: {
                    'timeonpage': timeonpage
                }
            }
    return credibility_dict


def R01_mental_extract(mental_result):
    mental_dict = {}
    for line in mental_result:
        sessionid = line[2]
        timeonpage = float(line[4])
        participant_id = int(line[len(line)-1])

        if participant_id in mental_dict:
            mental_dict[participant_id][sessionid] = {'timeonpage': timeonpage}
        else:
            mental_dict[participant_id] = {
                sessionid:{
                    'timeonpage': timeonpage
                }
            }
    return mental_dict


def R01_trial_extract(trial_result):
    ##########################################################################################
    # 1. rt: react time
    # 2. rt_correct: react time of the first attempt
    # 3. time_elapsed: accumulate time of rt
    # 4. unit: millisecond
    ##########################################################################################
    enroll_condition = {}
    trial_dict = {}
    for line in trial_result:
        sessionid = line[2]
        first_try_correct = line[6] # called correct in the db
        rt_correct = float(line[10])/1000 # called rt in the db
        time_elapsed = float(line[13])/1000
        participant_id = int(line[16])

        if participant_id in trial_dict:
            if sessionid in trial_dict[participant_id]:
                trial_dict[participant_id][sessionid]['time_elapsed'].append(time_elapsed)
                trial_dict[participant_id][sessionid]['first_try_correct'].append(first_try_correct)
                trial_dict[participant_id][sessionid]['rt_correct'].append(rt_correct)
            else:
                trial_dict[participant_id][sessionid] = {
                    'time_elapsed': [time_elapsed],
                    'first_try_correct': [first_try_correct],
                    'rt_correct': [rt_correct]
                }
        else:
            trial_dict[participant_id] = {
                sessionid:
                {
                'time_elapsed': [time_elapsed],
                'first_try_correct': [first_try_correct],
                'rt_correct': [rt_correct]
                }
            }

    return trial_dict


def R01_training_extract(training_result):
    training_dict = {}
    
    for line in training_result:
        sessionid = line[2]
        participant_id = int(line[21])
        latency = line[19]
        trial_type = line[20]
        first_react = line[10]
        trial_id = line[0]
        correct = line[7]
        letter_latency_time_first = 60
        letter_latency_time = 60
        question_latency_time_first = 60
        question_latency_time = 60

        if trial_type == 'MissingLetter':
            letter_latency_time_first = int(np.ceil(int(first_react)/1000))
            letter_latency_time = int(np.ceil(int(latency)/1000))
            question_latency_time_first = 0.0
            question_latency_time = 0.0
        
        if trial_type == 'Question':
            letter_latency_time_first = 0
            letter_latency_time = 0
            question_latency_time_first = int(np.ceil(int(first_react)/1000))
            question_latency_time = int(np.ceil(int(latency)/1000))

        if participant_id in training_dict:
            if sessionid in training_dict[participant_id]:
                training_dict[participant_id][sessionid][trial_id] = {
                    'letter_latency_first': letter_latency_time_first,
                    'letter_latency': letter_latency_time,
                    'question_latency_first': question_latency_time_first,
                    'question_latency': question_latency_time,
                    'correct': correct
                }
            else:
                training_dict[participant_id][sessionid] = {
                    trial_id: {
                        'letter_latency_first': letter_latency_time_first,
                        'letter_latency': letter_latency_time,
                        'question_latency_first': question_latency_time_first,
                        'question_latency': question_latency_time,
                        'correct': correct
                    }
                }
        else:
            training_dict[participant_id] = {
                sessionid: {
                    trial_id: {
                        'letter_latency_first': letter_latency_time_first,
                        'letter_latency': letter_latency_time,
                        'question_latency_first': question_latency_time_first,
                        'question_latency': question_latency_time,
                        'correct': correct
                    }
                }
            }

    return training_dict
            

def feature_vector_r01_overlap_with_mindtrails(RR_dict, BBSIQ_dict, OASIS_dict, demographics_dict, timeOnPage_dict):
    task_dict = {
        'preTest': ['RR', 'BBSIQ', 'OASIS', 'demographics'],
        'firstSession': ['OASIS']
    }
    education_level = {'Prefer not to answer': 0, '555': 0, 'Elementary School': 1, 'Some High School': 2,
                       'High School Graduate': 3, 'Some College': 4, "Associate's Degree": 5, 'Some Graduate School': 6,
                       "Bachelor's Degree": 7, 'M.B.A.': 8, "Master's Degree": 9, 'Ph.D.': 10, 'J.D.': 11,
                       'M.D.': 12, 'Other': 13}
    income_level = {'Less than $5,000': 0, '$5,000 through $11,999': 1, '$12,000 through $15,999': 2,
                    '$16,000 through $24,999': 3, '$25,000 through $34,999': 4, '$35,000 through $49,999': 5,
                    '$50,000 through $74,999': 6, '$75,000 through $99,999': 7, '$100,000 through $149,999': 8,
                    '$150,000 through $199,999': 9, '$200,000 through $249,999': 10, '$250,000 or greater': 11,
                    'Other': 12, "Don't know": 13, 'Prefer not to answer': 14, '555':14}

    feature_item_list, single_e_feature_vector = [], []

    for session in ['preTest', 'firstSession']:  # all sessions before prediction session
        for questionnaire in task_dict[session]:
            if questionnaire == 'demographics':
                demographics_items = ['education', 'income']
                demographics_values = {}
                # get values
                for item in demographics_items:
                    value = None
                    if item not in demographics_dict:
                        value = 'Other'
                    else:
                        value = demographics_dict[item]

                    if ('?' in value) or (value == '') or (value == 'Junior High') or ('Other' in value):
                        demographics_values[item] = 'Other'
                    else:
                        demographics_values[item] = value
                # append values to vector
                for item in demographics_items:
                    if item == 'education':
                        single_e_feature_vector.append(education_level[demographics_values[item]])
                        feature_item_list.append(session + '_' + questionnaire + '_edu')
                    elif item == 'income':
                        single_e_feature_vector.append(income_level[demographics_values[item]])
                        feature_item_list.append(session + '_' + questionnaire + '_income')  ##

            elif questionnaire == 'RR':
                target_value_list = []
                non_target_value_list = []

                if session in RR_dict:
                    for RR_item in RR_dict[session]:
                        if np.isnan(RR_dict[session][RR_item]) == False:
                            if '_NS' in RR_item:
                                target_value_list.append(RR_dict[session][RR_item])
                            elif '_PS' in RR_item:
                                non_target_value_list.append(RR_dict[session][RR_item])
                    if np.mean(non_target_value_list) != 0.0:
                        single_e_feature_vector.append(np.mean(target_value_list) / np.mean(non_target_value_list))
                    else:
                        single_e_feature_vector.append(0.0)
                else:
                    single_e_feature_vector.append(0.0)

                feature_item_list.append(session + '_' + questionnaire)

            elif questionnaire == 'BBSIQ':
                physical_list = ['breath_suffocate', 'chest_heart', 'confused_outofmind', 'dizzy_ill',
                                 'heart_wrong',
                                 'lightheaded_faint', 'vision_illness']

                non_physical_list = ['breath_flu', 'breath_physically', 'vision_glasses', 'vision_strained',
                                     'lightheaded_eat', 'lightheaded_sleep', 'chest_indigestion', 'chest_sore',
                                     'heart_active', 'heart_excited', 'confused_cold', 'confused_work', 'dizzy_ate',
                                     'dizzy_overtired']

                threat_list = ['visitors_bored', 'shop_irritating', 'smoke_house', 'friend_incompetent',
                               'jolt_burglar', 'party_boring', 'urgent_died']

                non_threat_list = ['visitors_engagement', 'visitors_outstay', 'shop_bored', 'shop_concentrating',
                                   'smoke_cig', 'smoke_food', 'friend_helpful', 'friend_moreoften', 'jolt_dream',
                                   'jolt_wind', 'party_hear', 'party_preoccupied', 'urgent_bill', 'urgent_junk']

                if session in BBSIQ_dict:
                    physical_value_list = []
                    non_physical_value_list = []
                    threat_value_list = []
                    non_threat_value_list = []

                    for item in BBSIQ_dict[session]:
                        if np.isnan(BBSIQ_dict[session][item]) == False:
                            if item in physical_list:
                                physical_value_list.append(BBSIQ_dict[session][item])
                            elif item in non_physical_list:
                                non_physical_value_list.append(BBSIQ_dict[session][item])
                            elif item in threat_list:
                                threat_value_list.append(BBSIQ_dict[session][item])
                            elif item in non_threat_list:
                                non_threat_value_list.append(BBSIQ_dict[session][item])

                    if np.mean(non_physical_value_list) != 0.0:
                        single_e_feature_vector.append(
                            np.mean(physical_value_list) / np.mean(non_physical_value_list))
                    else:
                        single_e_feature_vector.append(0.0)

                    if np.mean(non_threat_value_list) != 0.0:
                        single_e_feature_vector.append(np.mean(threat_value_list) / np.mean(non_threat_value_list))
                    else:
                        single_e_feature_vector.append(0.0)

                else:
                    single_e_feature_vector.append(0.0)
                    single_e_feature_vector.append(0.0)

                feature_item_list.append(session + '_' + questionnaire + '_physical')
                feature_item_list.append(session + '_' + questionnaire + '_threat')

            elif questionnaire == 'OASIS':
                if session in OASIS_dict:
                    values = []
                    for item in OASIS_dict[session]:
                        if np.isnan(OASIS_dict[session][item]) == False:
                            values.append(OASIS_dict[session][item])
                    single_e_feature_vector.append(np.sum(values))
                else:
                    single_e_feature_vector.append(0.0)
                feature_item_list.append(session + '_' + questionnaire)


    return single_e_feature_vector, feature_item_list

def feature_vector_r01_overlap_with_templeton(credibility_dict, mental_dict, affect_dict, trial_dict, demographics_dict):
    task_dict = {
        'preTest': ['credibility', 'demographics', 'mental'],
        'firstSession': ['affect_pre', 'trial', 'affect_post']
    }
    education_level = {'Prefer not to answer': 0, '555': 0, 'Elementary School': 1, 'Some High School': 2,
                       'High School Graduate': 3, 'Some College': 4, "Associate's Degree": 5, 'Some Graduate School': 6,
                       "Bachelor's Degree": 7, 'M.B.A.': 8, "Master's Degree": 9, 'Ph.D.': 10, 'J.D.': 11,
                       'M.D.': 12, 'Other': 13}
    income_level = {'Less than $5,000': 0, '$5,000 through $11,999': 1, '$12,000 through $15,999': 2,
                    '$16,000 through $24,999': 3, '$25,000 through $34,999': 4, '$35,000 through $49,999': 5,
                    '$50,000 through $74,999': 6, '$75,000 through $99,999': 7, '$100,000 through $149,999': 8,
                    '$150,000 through $199,999': 9, '$200,000 through $249,999': 10, '$250,000 or greater': 11,
                    'Other': 12, "Don't know": 13, 'Prefer not to answer': 14, '555':14}

    feature_item_list, single_e_feature_vector = [], []

    for session in ['preTest', 'firstSession']:
        for questionnaire in task_dict[session]:
            if questionnaire == 'demographics':
                demographics_items = ['education', 'income', 'timeonpage']
                demographics_values = {}
                for item in demographics_items:
                    value = None
                    if item not in demographics_dict:
                        value = 'Other'
                    else:
                        value = demographics_dict[item]

                    if (item != 'timeonpage') and ( ('?' in value) or (value == '') or (value == 'Junior High') or ('Other' in value) ):
                        demographics_values[item] = 'Other'
                    else:
                        demographics_values[item] = value

                for item in demographics_items:
                    if item == 'education':
                        single_e_feature_vector.append(education_level[demographics_values[item]])
                        feature_item_list.append(session + '_' + questionnaire + '_edu')
                    elif item == 'income':
                        single_e_feature_vector.append(income_level[demographics_values[item]])
                        feature_item_list.append(session + '_' + questionnaire + '_income')
                    elif item == 'timeonpage':
                        single_e_feature_vector.append(demographics_values['timeonpage'])
                        feature_item_list.append(session + '_' + questionnaire + '_timeonpage')
            elif questionnaire == 'credibility':
                if session in credibility_dict:
                    single_e_feature_vector.append(credibility_dict[session]['timeonpage'])
                else:
                    single_e_feature_vector.append(0.0)

                feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

            elif questionnaire == 'mental':
                if session in mental_dict:
                    single_e_feature_vector.append(mental_dict[session]['timeonpage'])
                else:
                    single_e_feature_vector.append(0.0)

                feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

            elif questionnaire == 'affect_pre':
                score_list = ['posFeelings', 'negFeelings']
                if session in affect_dict and 'pre' in affect_dict[session]:
                    for score_item in score_list:
                        single_e_feature_vector.append(affect_dict[session]['pre'][score_item])

                    single_e_feature_vector.append(affect_dict[session]['pre']['timeonpage'])  # probably can remove

                else:
                    for l in range(3):
                        single_e_feature_vector.append(0.0)

                for score_item in score_list:
                    feature_item_list.append(session + '_' + questionnaire + '_' + score_item)
                feature_item_list.append(session + '_' + questionnaire + '_timeonpage')  # probably can remove

            elif questionnaire == 'affect_post':
                score_list = ['posFeelings', 'negFeelings']
                if session in affect_dict and 'post' in affect_dict[session]:
                    for score_item in score_list:
                        single_e_feature_vector.append(affect_dict[session]['post'][score_item])

                    single_e_feature_vector.append(affect_dict[session]['post']['timeonpage'])  # probably can remove

                else:
                    for l in range(3):
                        single_e_feature_vector.append(0.0)

                for score_item in score_list:
                    feature_item_list.append(session + '_' + questionnaire + '_' + score_item)
                feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

            elif questionnaire == 'trial':
                if session in trial_dict:
                    if 'first_try_correct' in trial_dict[session]:
                        number_correctness = trial_dict[session]['first_try_correct'].count('TRUE')
                        single_e_feature_vector.append(number_correctness)
                    else:
                        single_e_feature_vector.append(0.0)
                    if ('time_elapsed' in trial_dict[session]) and (len(trial_dict[session]['time_elapsed']) > 1):
                        time_elapsed_list = []
                        for i in range(len(trial_dict[session]['time_elapsed'])):
                            if i == 0:
                                time_elapsed_list.append(trial_dict[session]['time_elapsed'][i])
                            else:
                                time_elapsed_list.append(
                                    trial_dict[session]['time_elapsed'][i] - trial_dict[session]['time_elapsed'][
                                        i - 1])
                        if len(time_elapsed_list) > 0:
                            single_e_feature_vector.append(np.mean(time_elapsed_list))
                            single_e_feature_vector.append(np.std(time_elapsed_list))
                            single_e_feature_vector.append(
                                trial_dict[session]['time_elapsed'][len(trial_dict[session]['time_elapsed']) - 1])
                        else:
                            for l in range(3):
                                single_e_feature_vector.append(0.0)
                    else:
                        for l in range(3):
                            single_e_feature_vector.append(0.0)
                else:
                    for l in range(4):
                        single_e_feature_vector.append(0.0)

                feature_item_list.append(session + '_' + questionnaire + '_first_try_correct')
                feature_item_list.append(session + '_' + questionnaire + '_latency_time_mean')
                feature_item_list.append(session + '_' + questionnaire + '_latency_time_std')
                feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

    return single_e_feature_vector, feature_item_list
