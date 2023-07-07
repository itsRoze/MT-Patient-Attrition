import numpy as np

def r01_mindtrails_feature_vector_generation(training_set_session, RR_dict, BBSIQ_dict, OASIS_dict, demographic_dict,
                                             dwell_time_dict, participant_list, dropout_label, prediction_session):
    feature_vector, truth_vector, feature_item_list = [], [], []
    task_dict = {
        'PRE': ['RR', 'BBSIQ', 'OASIS', 'demographic'],
        'SESSION1': ['OASIS'],
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
    for e in participant_list:
        feature_item_list = []
        if dropout_label[e][prediction_session] == '1':
            truth_vector.append(1)
        else:
            truth_vector.append(0)

        single_e_feature_vector = []
        for session in training_set_session:  # all sessions before prediction session
            for questionnaire in task_dict[session]:
                if questionnaire == 'demographic':
                    demographic_items = ['education', 'income']
                    demographic_values = {}
                    if e in demographic_dict:
                        for item in demographic_items:
                            value = None
                            if item not in demographic_dict[e]:
                                value = 'Other'
                            else:
                                value = demographic_dict[e][item]

                            if ('?' in value) or (value == '') or (value == 'Junior High') or ('Other' in value):
                                demographic_values[item] = 'Other'
                            else:
                                demographic_values[item] = value
                    else:
                        for item in demographic_items:
                            demographic_values[item] = 'Other'

                    for item in demographic_items:
                        if item == 'education':
                            single_e_feature_vector.append(education_level[demographic_values[item]])
                            feature_item_list.append(session + '_' + questionnaire + '_edu')
                        elif item == 'income':
                            single_e_feature_vector.append(income_level[demographic_values[item]])
                            feature_item_list.append(session + '_' + questionnaire + '_income')

                elif questionnaire == 'RR':
                    target_value_list = []
                    non_target_value_list = []

                    if e in RR_dict and session in RR_dict[e]:
                        for RR_item in RR_dict[e][session]:
                            if np.isnan(RR_dict[e][session][RR_item]) == False:
                                if '_NS' in RR_item:
                                    target_value_list.append(RR_dict[e][session][RR_item])
                                elif '_PS' in RR_item:
                                    non_target_value_list.append(RR_dict[e][session][RR_item])
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

                    if e in BBSIQ_dict and session in BBSIQ_dict[e]:
                        physical_value_list = []
                        non_physical_value_list = []
                        threat_value_list = []
                        non_threat_value_list = []

                        for item in BBSIQ_dict[e][session]:
                            if np.isnan(BBSIQ_dict[e][session][item]) == False:
                                if item in physical_list:
                                    physical_value_list.append(BBSIQ_dict[e][session][item])
                                elif item in non_physical_list:
                                    non_physical_value_list.append(BBSIQ_dict[e][session][item])
                                elif item in threat_list:
                                    threat_value_list.append(BBSIQ_dict[e][session][item])
                                elif item in non_threat_list:
                                    non_threat_value_list.append(BBSIQ_dict[e][session][item])

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
                    if e in OASIS_dict and session in OASIS_dict[e]:
                        values = []
                        for item in OASIS_dict[e][session]:
                            if np.isnan(OASIS_dict[e][session][item]) == False:
                                values.append(OASIS_dict[e][session][item])
                        single_e_feature_vector.append(np.sum(values))
                    else:
                        single_e_feature_vector.append(0.0)
                    feature_item_list.append(session + '_' + questionnaire)

                elif questionnaire == 'dwell_time':
                    if e in dwell_time_dict and session in dwell_time_dict[e]:
                        single_e_feature_vector.append(dwell_time_dict[int(e)][session]['DURATION'])
                    else:
                        single_e_feature_vector.append(0.0)

                    feature_item_list.append(session + '_' + questionnaire + '_dwell_time')

        feature_vector.append(single_e_feature_vector)

    return feature_vector, truth_vector, feature_item_list

def r01_templeton_feature_vector_generation(training_set_session, prediction_session, participant_list, credibility_dict, mental_dict, whatibelieve_dict, affect_dict, trial_dict, demographic_dict, session_completion_dict, dropout_label):
    feature_vector, truth_vector, feature_item_list = [], [], []

    task_dict = {
        'preTest': ['credibility', 'demographic', 'mental'],
        'firstSession': ['affect_pre', 'trial', 'affect_post'],
        'secondSession': ['affect_pre', 'trial', 'affect_post'],
    }

    education_level = {'Prefer not to answer': 0, '555':0, 'Elementary School': 1, 'Some High School': 2,
                       'High School Graduate': 3, 'Some College': 4, "Associate's Degree": 5, 'Some Graduate School': 6,
                       "Bachelor's Degree": 7, 'M.B.A.': 8, "Master's Degree": 9, 'Ph.D.': 10, 'J.D.': 11,
                       'M.D.': 12, 'Other': 13}
    income_level = {'Less than $5,000': 0, '$5,000 through $11,999': 1, '$12,000 through $15,999': 2,
                    '$16,000 through $24,999': 3, '$25,000 through $34,999': 4, '$35,000 through $49,999': 5,
                    '$50,000 through $74,999': 6, '$75,000 through $99,999': 7, '$100,000 through $149,999': 8,
                    '$150,000 through $199,999': 9, '$200,000 through $249,999': 10, '$250,000 or greater': 11,
                    'Other': 12, "Don't know": 13, 'Prefer not to answer': 14, '555':14}

    for e in participant_list:
        feature_item_list = []
        if dropout_label[e][prediction_session] == '1':
            truth_vector.append(1)
        else:
            truth_vector.append(0)

        single_e_feature_vector = []

        for session in training_set_session:
            for questionnaire in task_dict[session]:
                if questionnaire == 'demographic':
                    demographic_items = ['education', 'income', 'timeonpage']
                    demographic_values = {}
                    if e in demographic_dict:
                        for item in demographic_items:
                            value = None
                            if item not in demographic_dict[e]:
                                value = 'Other'
                            else:
                                value = demographic_dict[e][item]

                            if item != 'timeonpage' and (('?' in value) or (value == '') or (value == 'Junior High') or ('Other' in value)):
                                demographic_values[item] = 'Other'
                            else:
                                demographic_values[item] = value
                    else:
                        for item in demographic_items:
                            demographic_values[item] = 'Other'
                        demographic_values['timeonpage'] = 3600*24*2

                    for item in demographic_items:
                        if item == 'education':
                            single_e_feature_vector.append(education_level[demographic_values[item]])
                            feature_item_list.append(session + '_' + questionnaire + '_edu')
                        elif item == 'income':
                            single_e_feature_vector.append(income_level[demographic_values[item]])
                            feature_item_list.append(session + '_' + questionnaire + '_income')
                        elif item == 'timeonpage':
                            single_e_feature_vector.append(demographic_values['timeonpage'])
                            feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

                elif questionnaire == 'credibility':
                    if e in credibility_dict and session in credibility_dict[e]:
                        single_e_feature_vector.append(credibility_dict[e][session]['timeonpage'])
                    else:
                        single_e_feature_vector.append(0.0)

                    feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

                elif questionnaire == 'mental':
                    if e in mental_dict and session in mental_dict[e]:
                        single_e_feature_vector.append(mental_dict[e][session]['timeonpage'])
                    else:
                        single_e_feature_vector.append(0.0)

                    feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

                elif questionnaire == 'affect_pre':
                    score_list = ['posFeelings', 'negFeelings']
                    if e in affect_dict and session in affect_dict[e] and 'pre' in affect_dict[e][session]:
                        for score_item in score_list:
                            single_e_feature_vector.append(affect_dict[e][session]['pre'][score_item])

                        single_e_feature_vector.append(affect_dict[e][session]['pre']['timeonpage'])

                    else:
                        for l in range(3):
                            single_e_feature_vector.append(0.0)

                    for score_item in score_list:
                        feature_item_list.append(session + '_' + questionnaire + '_' + score_item)
                    feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

                elif questionnaire == 'affect_post':
                    score_list = ['posFeelings', 'negFeelings']
                    if e in affect_dict and session in affect_dict[e] and 'post' in affect_dict[e][session]:
                        for score_item in score_list:
                            single_e_feature_vector.append(affect_dict[e][session]['post'][score_item])

                        single_e_feature_vector.append(affect_dict[e][session]['post']['timeonpage'])

                    else:
                        for l in range(3):
                            single_e_feature_vector.append(0.0)

                    for score_item in score_list:
                        feature_item_list.append(session + '_' + questionnaire + '_' + score_item)
                    feature_item_list.append(session + '_' + questionnaire + '_timeonpage')

                elif questionnaire == 'trial':
                    if e in trial_dict and session in trial_dict[e]:
                        if 'first_try_correct' in trial_dict[e][session]:
                            number_correctness = trial_dict[e][session]['first_try_correct'].count('TRUE')
                            single_e_feature_vector.append(number_correctness)
                        else:
                            single_e_feature_vector.append(0.0)
                        if ('time_elapsed' in trial_dict[e][session]) and (len(trial_dict[e][session]['time_elapsed']) > 1):
                            time_elapsed_list = []
                            for i in range(len(trial_dict[e][session]['time_elapsed'])):
                                if i == 0:
                                    time_elapsed_list.append(trial_dict[e][session]['time_elapsed'][i])
                                else:
                                    time_elapsed_list.append(
                                        trial_dict[e][session]['time_elapsed'][i] - trial_dict[e][session]['time_elapsed'][i - 1])
                            if len(time_elapsed_list) > 0:
                                single_e_feature_vector.append(np.mean(time_elapsed_list))
                                single_e_feature_vector.append(np.std(time_elapsed_list))
                                single_e_feature_vector.append(trial_dict[e][session]['time_elapsed'][len(trial_dict[e][session]['time_elapsed']) - 1])
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

        feature_vector.append(single_e_feature_vector)

    return feature_vector, truth_vector, feature_item_list
