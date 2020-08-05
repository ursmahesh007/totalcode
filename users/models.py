'''
A model is the single, definitive source of information about your data. 
It contains the essential fields and behaviors of the data you’re storing. 
Generally, each model maps to a single database table.

The basics:
Each model is a Python class that subclasses django.db.models.Model.
Each attribute of the model represents a database field.
With all of this, Django gives you an automatically-generated database-access API.

https://docs.djangoproject.com/en/3.0/topics/db/models/
'''
# users/models.py
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.db import models
from djongo import models
import datetime

# Create your models here.
class CustomUser(AbstractUser):    
    age_range = ((1, "1-3"), (2, "4-8"), (3, "9-13"), (4, "14-18"), (5, "19-30"), (6, "31-50"), (7, "51-99"))
    genders = ((1, "Male"), (2, "Female"))
    height_range = ((1, "4'0\" - 4'11\""), (2, "5'0\" - 5'11\""), (3, "6'0\" - 6'11\""), (4, "7'0\" - 7'11\""))
    weight_range = ((1, "Below 150lb"), (2, "150lb to 200lb"), (3, "Over 200lb"))
    activity = ((1, "Sedentary"), (2, "Moderate"), (3, "Active"))
    diet = ((1, "Vegan"), (2, "Vegetarian"), (3, "Halal"), (4, "Meat"), (5, "Kosher"))
    
    email = models.CharField(max_length = 32, unique=True)
    first_name = models.CharField(max_length = 32, default = '', blank = True)
    last_name = models.CharField(max_length = 32, default = '', blank = True)
    age = models.IntegerField(choices = age_range, null = True, blank = True)
    gender = models.IntegerField(choices = genders, null = True, blank = True)
    height = models.IntegerField(choices = height_range, null = True, blank = True)
    weight = models.IntegerField(choices = weight_range, null = True, blank = True)
    activity = models.IntegerField(choices = activity, null = True, blank = True)
    dietary_preference = models.IntegerField(choices = diet, null = True, blank = True)
    allergic_food = models.ListField(default = list, null = True, blank = True)

    def __str__(self):
        return str(self.id)

class AllergyMapping(models.Model):
    milk = models.IntegerField()
    egg = models.IntegerField()
    peanut = models.IntegerField()
    tree_nut = models.IntegerField()
    soy = models.IntegerField()
    wheat = models.IntegerField()
    fish = models.IntegerField()
    shellfish = models.IntegerField()
    msg_monosodium_glutamate = models.IntegerField()
    high_fructose_corn_syrup_hfcs = models.IntegerField()
    mustard = models.IntegerField()
    celery = models.IntegerField()
    sesame = models.IntegerField()
    gluten = models.IntegerField()
    red_yellow_blue_dye = models.IntegerField()
    gluten_free_per_fda = models.IntegerField()
    non_gmo_claim = models.IntegerField()

    class Meta:
        db_table = 'foodallergies'
        managed = False

class ServiceMenuitemsFlat(models.Model):
    location_id= models.IntegerField(blank = True, null = True)
    location_name= models.CharField(max_length = 256, blank = True, null = True)
    location= models.CharField(max_length = 256, blank = True, null = True)
    service_menu_id= models.IntegerField(blank = True, null = True)
    service_date= models.CharField(max_length = 256, blank = True, null = True)
    meal_period_id= models.IntegerField(blank = True, null = True)
    meal_period= models.CharField(max_length = 256, blank = True, null = True)
    service_area_id= models.IntegerField(blank = True, null = True)
    service_area_name= models.CharField(max_length = 256, blank = True, null = True)
    sub_location_id= models.IntegerField(blank = True, null = True)
    sub_location_order= models.IntegerField(blank = True, null = True)
    sub_location_name= models.CharField(max_length = 256, blank = True, null = True)
    sub_location= models.CharField(max_length = 256, blank = True, null = True)
    menu_item_order= models.CharField(max_length = 256, blank = True, null = True)
    service_menu_item_id= models.IntegerField(blank = True, null = True)
    master_system_id= models.IntegerField(blank = True, null = True)
    recipe_id= models.CharField(max_length = 256, blank = True, null = True)
    recipe_name= models.CharField(max_length = 256, blank = True, null = True)
    recipe_marketing_name= models.CharField(max_length = 256, blank = True, null = True)
    recipe_short_name= models.CharField(max_length = 256, blank = True, null = True)
    production_area_id= models.IntegerField(blank = True, null = True)
    production_area_name= models.CharField(max_length = 256, blank = True, null = True)
    is_mto= models.CharField(max_length = 256, blank = True, null = True)
    serving_size_uom_id= models.IntegerField(blank = True, null = True)
    number_of_servings= models.CharField(max_length = 256, blank = True, null = True)
    serving_size_number= models.CharField(max_length = 256, blank = True, null = True)
    serving_size_description= models.CharField(max_length = 256, blank = True, null = True)
    serving_size_fraction_id= models.IntegerField(blank = True, null = True)
    service_size_fraction_description= models.CharField(max_length = 256, blank = True, null = True)
    serving_size_display= models.CharField(max_length = 256, blank = True, null = True)
    is_temp_required= models.CharField(max_length = 256, blank = True, null = True)
    food_cost= models.FloatField(blank = True, null = True)
    acceptability_factor= models.FloatField(blank = True, null = True)
    planned_count= models.FloatField(blank = True, null = True)
    prep_count= models.FloatField(blank = True, null = True)
    sold_count= models.FloatField(blank = True, null = True)
    on_hand_count= models.FloatField(blank = True, null = True)
    leftover_count= models.FloatField(blank = True, null = True)
    waste_count= models.FloatField(blank = True, null = True)
    smi_row_no= models.IntegerField(blank = True, null = True)
    is_result_required= models.CharField(max_length = 256, blank = True, null = True)
    comments= models.CharField(max_length = 256, blank = True, null = True)

    class Meta:
        managed = False
        db_table = 'serviceMenuitemsFlat'

class RecommendedFood(models.Model):
    location_id = models.IntegerField()
    recipe_id = models.CharField(max_length = 256, unique=True)
    serving_size_number = models.CharField(max_length = 256, unique=True)
    recipe_fraction_description = models.CharField(max_length = 256, default = '', blank = True)
    description = models.CharField(max_length = 256, default = '', blank = True)
    recipe_name = models.CharField(max_length = 256, default = '', blank = True)
    marketing_name = models.CharField(max_length = 256, default = '', blank = True)
    marketing_description = models.CharField(max_length = 256, default = '', blank = True)
    ingredient_statement = models.CharField(max_length = 256, default = '', blank = True)
    allergen_attributes = models.CharField(max_length = 256)
    dietary_attributes = models.CharField(max_length = 256)
    primary_attributes = models.CharField(max_length = 256)
    avg_rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'serviceRecipeNutrition'

class NewRecipe(models.Model):
    recipe_id= models.CharField(max_length = 256, blank = True, null = True)
    recipe_name= models.CharField(max_length = 256, blank = True, null = True)
    primary_attributes=  models.CharField(max_length = 256)
    ingredients=  models.CharField(max_length = 256)
    recipe_HEI_score= models.FloatField(blank = True, null = True)
    norm_HEI_score= models.FloatField(blank = True, null = True)

    class Meta:
        managed = False
        db_table = 'new_recipes'

class Meals(models.Model):
    recipe_id = models.CharField(max_length = 256, unique=True, primary_key=True)
    recipe_name = models.CharField(max_length = 256)
    marketing_description = models.CharField(max_length = 256)
    allergen_attributes = models.CharField(max_length = 256)
    dietary_attributes = models.CharField(max_length = 256)
    avg_rating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'serviceRecipeNutrition'

    def __str__(self):
        return str(self.recipe_id) + ": " + str(self.recipe_name)

class Rating(models.Model):
    meals = ((1, "Breakfast"), (2, "Lunch"), (3, "Dinner"), (4, "Snack"))
    profile_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
    recipe_id = models.ForeignKey(Meals,on_delete=models.CASCADE,db_constraint=False,to_field="recipe_id")
    meal_period = models.IntegerField(choices = meals, null = True, blank = True)
    rating = models.FloatField()

    def __str__(self):
        return str(self.rating)   

class CustomRecipe(models.Model):
    recipe_name = models.CharField(max_length = 64)
    recipe_description = models.CharField(max_length = 256, default = '', blank = True)
    preparation_time  = models.CharField(max_length = 256, default = '', blank = True)
    calories_per_serving = models.FloatField()
    number_of_servings = models.FloatField()

    def __str__(self):
        return str(self.id) + ": " + str(self.recipe_name)

class Diary(models.Model):
    meals = ((1, "Breakfast"), (2, "Lunch"), (3, "Dinner"), (4, "Snack"))

    # timestamp_entry = models.DateTimeField(max_length=16, null = True)
    timestamp_millis = models.BigIntegerField(null = True)
    profile_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meal_period = models.IntegerField(choices = meals, null = True, blank = True)
    is_custom_recipe = models.BooleanField(default = False)
    custom_recipe = models.ManyToManyField(CustomRecipe, blank = True)
    meals = models.ManyToManyField(Meals)

    

    
    
    # username = None
    # email = models.EmailField(_('email address'), unique=True)
    # USERNAME_FIELD = 'email' 

class UserInformation(models.Model):
    genders = (("F", "Female"), ("M", "Male"))
    levels = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

    # profile_id = models.PositiveIntegerField(blank = True, null = True)
    # allergic_food = ArrayField(models.CharField(max_length=10, blank=True), size=8, default = list,)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank = True, null = True)
    height = models.FloatField(help_text="Please use centimeters",default = 0, blank = True, null = True)
    weight = models.FloatField(help_text="Please use lbs",default = 0, blank = True, null = True)
    gender = models.CharField(max_length = 1, choices = genders, default = '', blank = True)
    target_calorie_intake = models.FloatField(default = 0,blank = True, null = True)
    preferred_meal = models.CharField(max_length = 30, default = '', blank = True)
    allergic_food = models.CharField(max_length = 30, default = '', blank = True)
    work_out_level = models.CharField(max_length = 1, choices = levels, help_text="With 5 being the highest", default = '', blank = True)
    dietary_preferences = models.CharField(max_length = 30, default = '', blank = True)
    health_history = models.CharField(max_length = 30, default = '', blank = True)
    preferred_breakfast_time = models.CharField(max_length = 30, default = '', blank = True)
    preferred_lunch_time = models.CharField(max_length = 30, default = '', blank = True)
    preferred_dinner_time = models.CharField(max_length = 30, default = '',blank = True)
    # class ReadonlyMeta:
    #     readonly = ["allergic_food"]
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['zip_code']

# class CalorieTracker(models.Model):
#     # ctracker_id = models.PositiveIntegerField(blank = True, null = True)
#     # profile_id = models.PositiveIntegerField(blank = True, null = True)
#     calorie_count = models.FloatField(blank = True, null = True)
#     date = models.DateField(blank = True, null = True)
#     consumed_calories = models.FloatField(blank = True, null = True)
#     remaining_calories = models.FloatField(blank = True, null = True)
#     total_calories = models.FloatField(blank = True, null = True)

# class FoodIntakeHistory(models.Model):
#     # intake_id = models.PositiveIntegerField(blank = True, null = True)
#     # profile_id = models.PositiveIntegerField(blank = True, null = True)
#     food_item = models.CharField(max_length=255, default = '', blank = True)
#     intake_time = models.DateField(blank = True, null = True)
#     intake_calories = models.FloatField(blank = True, null = True)

# class FoodMenu(models.Model):
#     # food_chart_id = models.PositiveIntegerField(blank = True, null = True)
#     cuisine_name = models.CharField(max_length=255, default = '')
#     ratings = models.CharField(max_length=255, default = '')
#     description = models.CharField(max_length=255, default = '')
#     calories = models.FloatField(blank = True, null = True)
#     carbs_count = models.FloatField(blank = True, null = True)
#     protein_count = models.FloatField(blank = True, null = True)
#     bar_code = models.PositiveIntegerField(blank = True, null = True)

# class FoodOrderHistory(models.Model):
#     # order_id = models.PositiveIntegerField(blank = True, null = True)
#     # profile_id = models.PositiveIntegerField(blank = True, null = True)
#     # food_chart_id = models.PositiveIntegerField(blank = True, null = True)
#     food_item = models.CharField(max_length=255, default = '')
#     order_time = models.DateField(blank = True, null = True)