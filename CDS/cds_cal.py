#!/usr/bin/env python
# coding: utf-8

# In[4]:


# Data Dictionary for Male and Female as per the excel sheet. 
# This dictionary will be pushed to MongoDb in future and then will be called from there. 

def cds_cal(gender,age,lifestyle,meal_time, service_recipe_nutrition, service_menu_items_flat, hei_file):
    from collections import defaultdict
    data = {
            'M': {
                '1-3': {
                    'Sedentary': '1000',
                    'Moderate': '1200',
                    'Active': '1200',
                    'Fiber': '14.0'
                    },
                '4-8': {
                    'Sedentary': '1320',
                    'Moderate': '1520',
                    'Active': '1760',
                    'Fiber': '19.6'
                    },
                '9-13': {
                    'Sedentary': '1760',
                    'Moderate': '2000',
                    'Active': '2280',
                    'Fiber': '25.2'
                    },
                '14-18': {
                    'Sedentary': '2280',
                    'Moderate': '2680',
                    'Active': '3080',
                    'Fiber': '30.8'
                    },
                '19-30': {
                    'Sedentary': '2466',
                    'Moderate': '2733',
                    'Active': '3000',
                    'Fiber': '33.6'
                    },
                '31-50': {
                    'Sedentary': '2300',
                    'Moderate': '2550',
                    'Active': '2850',
                    'Fiber': '30.8'
                    },
                '51-99': {
                    'Sedentary': '2066',
                    'Moderate': '2300',
                    'Active': '2600',
                    'Fiber': '28.0'
                    }
                },
        'F': {
                '1-3': {
                    'Sedentary': '1000',
                    'Moderate': '1100',
                    'Active': '1200',
                    'Fiber': '14.0'
                    },
                '4-8': {
                    'Sedentary': '1240',
                    'Moderate': '1480',
                    'Active': '1640',
                    'Fiber': '16.8'
                    },
                '9-13': {
                    'Sedentary': '1520',
                    'Moderate': '1840',
                    'Active': '2040',
                    'Fiber': '22.4'
                    },
                '14-18': {
                    'Sedentary': '1800',
                    'Moderate': '2000',
                    'Active': '2400',
                    'Fiber': '25.2'
                    },
                '19-30': {
                    'Sedentary': '1933',
                    'Moderate': '2133',
                    'Active': '2400',
                    'Fiber': '28.0'
                    },
                '31-50': {
                    'Sedentary': '1800',
                    'Moderate': '2000',
                    'Active': '2200',
                    'Fiber': '25.2'
                    },
                '51-99': {
                    'Sedentary': '1600',
                    'Moderate': '1800',
                    'Active': '2066',
                    'Fiber': '22.4'
                    }
                }
            }          

    # Function to calcuate the ideal Macros based on Age, Gender and Lifestyle for a day.

    def get_ideal_daily_macros(gender,age,lifestyle):

        # Call the get_cal function to get the calories for the given gender, age and lifestyle
        cals=int(data[gender][age][lifestyle])

        # As per standards protein intake should be minimum of 10 percent of dailay calorie intake
        cal_in_protein = cals * 0.1
        # As per standards, 1 gram of protein contains 4 calories
        protein_in_grams = cal_in_protein / 4

        # As per standards carb intake should be minimum of 45 percent of dailay calorie intake
        cal_in_carbs = cals * 0.45
        # As per standards, 1 gram of carb contains 4 calories
        carbs_in_grams = cal_in_carbs / 4

        # As per standards saturated fat intake should be minimum of 5 percent of dailay calorie intake
        cal_in_sat_fat = cals * 0.05
        # As per standards, 1 gram of saturated contains 9 calories
        sat_fat_in_grams = cal_in_sat_fat / 9

        # As per standards added sugar intake should be minimum of 5 percent of dailay calorie intake
        cal_in_sugar = cals * 0.05
        # As per standards, 1 gram of added sugar contains 4 calories
        sugar_in_grams = cal_in_sugar / 4

        # Call age_range function to calculate the age group of the person, this is required to calculate total fat
        # Total fat is different for different age groups. 


        if age == '1-3':
            cal_in_tfat = cals * 0.3
            tfat_in_grams = cal_in_tfat / 9
        if age in ['4-8','9-13','14-18']:
            cal_in_tfat = cals * 0.25
            tfat_in_grams = cal_in_tfat / 9
        if age in ['19-30','31-50','51-99']:
            cal_in_tfat = cals * 0.2
            tfat_in_grams = cal_in_tfat / 9

        # calcluate fiber based on gender and age group.    
        fiber_in_grams =  float(data[gender][age]['Fiber'])

        return [protein_in_grams,carbs_in_grams,sat_fat_in_grams,sugar_in_grams,fiber_in_grams,tfat_in_grams]

    #Function to calculate ideal Macros for Breakfast

    def get_daily_ideal_bf(gender, age, lifestyle):
        ideal_bf={}

        ideal_macros = get_ideal_daily_macros(gender, age, lifestyle)
        ideal_bf['protein'] = ideal_macros[0] / 5
        ideal_bf['carbohydrate'] = ideal_macros[1] / 5
        ideal_bf['saturated_fat'] = ideal_macros[2] / 5
        ideal_bf['total_sugars'] = ideal_macros[3] / 5
        ideal_bf['fiber'] = ideal_macros[4] / 5
        ideal_bf['total_fat'] = ideal_macros[5] / 5
        return ideal_bf

    def get_daily_ideal_lunch(gender, age, lifestyle):
        ideal_lunch={}
        ideal_macros = get_ideal_daily_macros(gender, age, lifestyle)
        ideal_lunch['protein'] = (ideal_macros[0] / 5)*2
        ideal_lunch['carbohydrate'] = (ideal_macros[1] / 5)*2
        ideal_lunch['saturated_fat'] = (ideal_macros[2] / 5)*2
        ideal_lunch['total_sugars'] = (ideal_macros[3] / 5)*2
        ideal_lunch['fiber'] = (ideal_macros[4] / 5)*2
        ideal_lunch['total_fat'] = (ideal_macros[5] / 5)*2
        return ideal_lunch

    def get_daily_ideal_dinner(gender, age, lifestyle):
        ideal_dinner={}
        ideal_macros = get_ideal_daily_macros(gender, age, lifestyle)
        ideal_dinner['protein'] = (ideal_macros[0] / 5)*2
        ideal_dinner['carbohydrate'] = (ideal_macros[1] / 5)*2
        ideal_dinner['saturated_fat'] = (ideal_macros[2] / 5)*2
        ideal_dinner['total_sugars'] = (ideal_macros[3] / 5)*2
        ideal_dinner['fiber'] = (ideal_macros[4] / 5)*2
        ideal_dinner['total_fat'] = (ideal_macros[5] / 5)*2
        return ideal_dinner



    meal_period_dict = defaultdict(set) 
    for d in service_menu_items_flat:
        meal_period_dict[d['recipe_id']].add(d['meal_period'])
        # if d['recipe_id'] not in meal_period_dict:
        #     meal_period_dict[d['recipe_id']].add(d['meal_period'])
        # else:
        #     meal_period_dict[d['recipe_id']].add(d['meal_period'])


    list_dict=[]
    for recipe in service_recipe_nutrition:
        dict1 = {}
        dict1['recipeid'] = recipe['recipe_id']
        dict1['recipe_name'] = recipe['recipe_name']
        dict1['serving_size_number'] = int(1 if recipe['serving_size_number'] is None else recipe['serving_size_number'])
        dict1['meal_period'] = list(meal_period_dict[recipe['recipe_id']])
        dict1['protein'] = recipe['primary_attributes']['protein']/dict1['serving_size_number']
        dict1['carbohydrate'] = recipe['primary_attributes']['carbohydrate']/dict1['serving_size_number']
        dict1['fiber'] = recipe['primary_attributes']['fiber']/dict1['serving_size_number']
        dict1['total_fat'] = recipe['primary_attributes']['total_fat']/dict1['serving_size_number']
        dict1['saturated_fat'] = recipe['primary_attributes']['saturated_fat']/dict1['serving_size_number']
        dict1['total_sugars'] = (int(0 if recipe['primary_attributes']['total_sugars'] is None else recipe['primary_attributes']['total_sugars']))/dict1['serving_size_number']
        dict1['marketing_description'] = recipe['marketing_description']
        dict1['allergen_attributes'] = recipe['allergen_attributes']
        dict1['dietary_attributes'] = recipe['dietary_attributes']
        list_dict.append(dict1)


    def diff_cal(gender,age,lifestyle,meal_time):
        cds_list = []
        receipe_list = []
        for i in range(len(list_dict)):
            cds_dict={}

            if list_dict[i]['recipeid'] not in receipe_list:
                receipe_list.append(list_dict[i]['recipeid'])
                if (meal_time == 'Breakfast') and (meal_time in list_dict[i]['meal_period']):
                    ideal_bf = get_daily_ideal_bf(gender,age,lifestyle)
                    protein = ((list_dict[i]['protein']- ideal_bf['protein'])/ideal_bf['protein'])*3
                    carbohydrate = ((list_dict[i]['carbohydrate']- ideal_bf['carbohydrate'])/ideal_bf['carbohydrate'])*2
                    fat = (((list_dict[i]['saturated_fat']- ideal_bf['saturated_fat'])/ideal_bf['saturated_fat']) + ((list_dict[i]['total_fat']- ideal_bf['total_fat'])/ideal_bf['total_fat'])) * 2 
                    sugar = ((list_dict[i]['total_sugars']- ideal_bf['total_sugars'])/ideal_bf['total_sugars'])*1
                    fiber = ((list_dict[i]['fiber']- ideal_bf['fiber'])/ideal_bf['fiber'])*1
                    for j in range(len(hei_file)):
                        if list_dict[i]['recipeid'] == hei_file[j]['recipe_id']:
                            hei = float(hei_file[j]['norm_HEI_score'])
                            break
                    cds_bf = protein + carbohydrate + fat + sugar + fiber + hei
                    cds_bf = round(cds_bf,2)
                    cds_dict['recipe_id'] = list_dict[i]['recipeid']
                    cds_dict['recipe_name'] = list_dict[i]['recipe_name']
                    cds_dict['recipe_id']
                    cds_dict['cds'] = round(cds_bf,2)
                    cds_dict['marketing_description'] = list_dict[i]['marketing_description']
                    cds_dict['allergen_attributes'] = list_dict[i]['allergen_attributes']
                    cds_dict['dietary_attributes'] = list_dict[i]['dietary_attributes']
                    cds_list.append(cds_dict)
                elif (meal_time == 'Lunch') and (meal_time in list_dict[i]['meal_period']):
                    ideal_lunch = get_daily_ideal_lunch(gender,age,lifestyle)
                    protein = ((list_dict[i]['protein']- ideal_lunch['protein'])/ideal_lunch['protein'])*3
                    carbohydrate = ((list_dict[i]['carbohydrate']- ideal_lunch['carbohydrate'])/ideal_lunch['carbohydrate'])*2
                    fat = (((list_dict[i]['saturated_fat']- ideal_lunch['saturated_fat'])/ideal_lunch['saturated_fat']) + ((list_dict[i]['total_fat']- ideal_lunch['total_fat'])/ideal_lunch['total_fat'])) * 2 
                    sugar = ((list_dict[i]['total_sugars']- ideal_lunch['total_sugars'])/ideal_lunch['total_sugars'])*1
                    fiber = ((list_dict[i]['fiber']- ideal_lunch['fiber'])/ideal_lunch['fiber'])*1
                    for j in range(len(hei_file)):
                        if list_dict[i]['recipeid'] == hei_file[j]['recipe_id']:
                            hei = float(hei_file[j]['norm_HEI_score'])
                            break
                    cds_lunch = protein + carbohydrate + fat + sugar + fiber + hei
                    cds_dict['recipe_id'] = list_dict[i]['recipeid']
                    cds_dict['recipe_name'] = list_dict[i]['recipe_name']
                    cds_dict['cds'] = round(cds_lunch,2)
                    cds_dict['marketing_description'] = list_dict[i]['marketing_description']
                    cds_dict['allergen_attributes'] = list_dict[i]['allergen_attributes']
                    cds_dict['dietary_attributes'] = list_dict[i]['dietary_attributes']
                    cds_list.append(cds_dict)
                elif (meal_time == 'Dinner') and (meal_time in list_dict[i]['meal_period']):
                    ideal_dinner = get_daily_ideal_dinner(gender,age,lifestyle)
                    protein = ((list_dict[i]['protein']- ideal_dinner['protein'])/ideal_dinner['protein'])*3
                    carbohydrate = ((list_dict[i]['carbohydrate']- ideal_dinner['carbohydrate'])/ideal_dinner['carbohydrate'])*2
                    fat = (((list_dict[i]['saturated_fat']- ideal_dinner['saturated_fat'])/ideal_dinner['saturated_fat']) + ((list_dict[i]['total_fat']- ideal_dinner['total_fat'])/ideal_dinner['total_fat'])) * 2 
                    sugar = ((list_dict[i]['total_sugars']- ideal_dinner['total_sugars'])/ideal_dinner['total_sugars'])*1
                    fiber = ((list_dict[i]['fiber']- ideal_dinner['fiber'])/ideal_dinner['fiber'])*1
                    for j in range(len(hei_file)):
                        if list_dict[i]['recipeid'] == hei_file[j]['recipe_id']:
                            hei = float(hei_file[j]['norm_HEI_score'])
                            break
                    cds_dinner = protein + carbohydrate + fat + sugar + fiber + hei
                    cds_dict['recipe_id'] = list_dict[i]['recipeid'] 
                    cds_dict['recipe_name'] = list_dict[i]['recipe_name']
                    cds_dinner = round(cds_dinner,2)
                    cds_dict['cds'] = cds_dinner
                    cds_dict['marketing_description'] = list_dict[i]['marketing_description']
                    cds_dict['allergen_attributes'] = list_dict[i]['allergen_attributes']
                    cds_dict['dietary_attributes'] = list_dict[i]['dietary_attributes']
                    cds_list.append(cds_dict)
        return (sorted(cds_list,reverse=True, key=lambda k: k['cds']) )
    return diff_cal(gender,age,lifestyle,meal_time)
