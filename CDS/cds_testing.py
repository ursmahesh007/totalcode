import cds_cal as cds
import json
from collections import OrderedDict 
from collections import defaultdict

with open("C:/Users/12678/Desktop/DXC/Aramark_data/aramark_data_0308_033120/aramark_data_new/service_menu_items/service_recipe_nutrition.json",'r') as file:
    service_recipe_nutrition = json.load(file)

with open("C:/Users/12678/Desktop/DXC/Aramark_data/aramark_data_0308_033120/aramark_data_new/service_menu_items/service_menu_items_flat_03_31_2020.json",'r') as file:
    service_menu_items_flat = json.load(file)

with open("C:/Users/12678/Desktop/DXC/Aramark_data/aramark_data_0308_033120/aramark_data_new/service_menu_items/new_recipes_0-1.json",'r') as file:
    hei_file = json.load(file)

cds_list=cds.cds_cal('M','19-30','Moderate','Breakfast',service_recipe_nutrition, service_menu_items_flat, hei_file)
print(cds_list)