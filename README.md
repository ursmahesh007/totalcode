# MarkoEatsBackend
This is the backend code for the MarkoEats application. This is done in python programming language and using the Django framework. Djongo allows usage of Django with MongoDB as our database, while DjangoRestFramework aids in creation of APIs.

UI reference: https://xd.adobe.com/view/e6c91497-f223-4eb6-57ca-3258834e9d73-90f8/

Replace the URL with these depending on which server is desired.
- 104.45.142.182 development server
- 40.112.53.149 test server
- 52.188.215.206 aramark alpha server


=======
# Changelog
1. Datetime to millis
2. Fixed bug in meals, avg_rating
3. Round avg_rating with one decimal place

# Dependencies
1. "pip install django 2.2.6" </br>
2. "pip install djongo 1.2.38" </br>
3. "pip install djangorestframework 3.10.3" </br>
4. "pip install django-crispy-forms 1.8.1" </br>
Use "pip freeze" to list dependencies in pip environment

# MANAGE.PY commands
Create changes to models: "python manage.py makemigrations polls" </br>
Apply changes in database: "python manage.py migrate" </br>
Create admin if needed: "python manage.py createsuperuser" </br>
Start development server: "python manage.py runserver" </br>

# FILES
Main files:
- settings.py
- models.py
- serializers.py
- views.py
- urls.py

Secondary files:
- admin.py
- apps.py
- forms.py

# API LIST:
1. [REGISTER](#register)
2. [LOGIN](#login)
3. [LOGOUT](#logout)
### [TOKEN USAGE USING POSTMAN](#token-usage-using-postman)
4. [USERS](#users)
5. [ALLERGYMAPPING](#allergymapping)
6. [RECOMMENDER](#recommender)
7. [RATING](#rating)
8. [MEALS](#meals)
9. [CUSTOM_RECIPE](#custom_recipe)
10. [DIARY](#diary)

## REGISTER
### (POST REQUEST): http://104.45.142.182/register/</br>
REGISTER USING POSTMAN: body, raw </br>

#### REQUEST
```
{
    "username": (username) <string>,
    "email": (email) <string>,
    "password": (password) <string>
}
```

#### RESPONSE SUCCESS
```
{
    "token": (token) <string>,
    "user": {
        "id": (token) <integer>,
        "username": (username) <string>,
        "email": (email) <string>
    }
}
```

#### RESPONSE USERNAME IN USE
```
{
    "code": 1 <integer>, 
    "error": "Username is already in use" <string>
}
```

#### RESPONSE EMAIL IN USE
```
{
    "code": 2 <integer>, 
    "error": "Email is already in use" <string>
}
```

## LOGIN

### (POST REQUEST): http://104.45.142.182/login/ </br>
LOGIN USING POSTMAN: body, raw </br>

#### REQUEST
```
{
    "username": (username) <string>,
    "password": (password) <string>
}
```

#### RESPONSE SUCCESS
```
{
    "status": true <boolean>,
    "token": (token) <string>,
    "user": {
        "id": (id) <integer>,
        "username": (username) <string>,
        "email": (email) <string>,
        "first_name": (first_name) <string>,
        "last_name": (test) <string>,
        "age": (1-7) <integer>,
        "gender": (1-2) <integer>,
        "height": (1-4) <integer>,
        "weight": (1-3) <integer>,
        "activity": (1-3) <integer>,
        "dietary_preference": (1-5) <integer>,
        "allergic_food": [
            <mapped integer>,
            <mapped integer>,
            ...
        ] <list>
    }
}
```
age_range = ((1, "1-3"), (2, "4-8"), (3, "9-13"), (4, "14-18"), (5, "19-30"), (6, "31-50"), (7, "51-99")) </br>
genders = ((1, "Male"), (2, "Female")) </br>
height_range = ((1, "4'0\" - 4'11\""), (2, "5'0\" - 5'11\""), (3, "6'0\" - 6'11\""), (4, "7'0\" - 7'11\"")) </br>
weight_range = ((1, "Below 150lb"), (2, "150lb to 200lb"), (3, "Over 200lb")) </br>
lifestyle = ((1, "Sedentary"), (2, "Moderate"), (3, "Active")) </br>
meals = ((1, "Vegan"), (2, "Vegetarian"), (3, "Halal"), (4, "Meat"), (5, "Kosher")) </br>

#### RESPONSE MISSING INFORMATION
```
{
    "code": 3,
    "error": "Missing profile information",
    "status": true <boolean>,
    "token": (token) <string>,
    "user": {
        "id": (id) <integer>,
        "username": (username) <string>,
        "email": (email) <string>,
        "first_name": (first_name) <string>,
        "last_name": (test) <string>,
        "age": (1-7) <integer>,
        "gender": (1-2) <integer>,
        "height": (1-4) <integer>,
        "weight": (1-3) <integer>,
        "activity": (1-3) <integer>,
        "dietary_preference": (1-5) <integer>,
        "allergic_food": [
            <mapped integer>,
            <mapped integer>,
            ...
        ]
    }
}
```

## LOGOUT

### (POST REQUEST): http://104.45.142.182/logout/ </br>
#### REQUEST
```
{
    "user_id": (user_id) <integer>,
    "token": (token) <string>
}
```

##### RESPONSE
```
{
    'success': 'Sucessfully logged out'
}
```

## TOKEN USAGE USING POSTMAN
TOKEN USING POSTMAN: headers </br>
Key: "Authorization" </br>
Value: "Token" (token) </br>
*Token will be needed to access API below.

## USERS

### (GET REQUEST) ALL USERS: http://104.45.142.182/admin/api/users/
#### RESPONSE
```
{
    "count": (count) <integer>,
    "next": (url of next page),
    "previous": (url of previous page),
    "results": [
        {
            "id": (id) <integer>,
            "email": (email) <string>,
            "username": (username) <string>,
            "first_name": (first_name) <string>,
            "last_name": (last_name) <string>,
            "age": (1-7) <integer>,
            "gender": (1-2) <integer>,
            "height": (1-4) <integer>,
            "weight": (1-3) <integer>,
            "activity": (1-3) <integer>,
            "dietary_preference": (1-5) <integer>,
            "allergic_food": [
                <mapped integer>,
                <mapped integer>,
                ...
            ]
        },
        {
            "id": (id) <integer>,
            "email": (email) <string>,
            "username": (username) <string>,
            "first_name": (first_name) <string>,
            "last_name": (last_name) <string>,
            "age": (1-7) <integer>,
            "gender": (1-2) <integer>,
            "height": (1-4) <integer>,
            "weight": (1-3) <integer>,
            "activity": (1-3) <integer>,
            "dietary_preference": (1-5) <mapped integer>,
            "allergic_food": [
                <mapped integer>,
                <mapped integer>,
                ...
            ]
        }
}
```

### (GET REQUEST) ONE USER: http://104.45.142.182/admin/api/users/3/ <--- specify user id
#### RESPONSE
```
{
    "id": (id) <integer>,
    "email": (email) <string>,
    "username": (username) <string>,
    "first_name": (first_name) <string>,
    "last_name": (last_name) <string>,
    "age": (1-7) <integer>,
    "gender": (1-2) <integer>,
    "height": (1-4) <integer>,
    "weight": (1-3) <integer>,
    "activity": (1-3) <integer>,
    "dietary_preference": (1-5) <mapped integer>,
    "allergic_food": [
        <mapped integer>,
        <mapped integer>,
        ...
    ]
}
```

### (POST REQUEST) CREATE USER: http://104.45.142.182/admin/api/users/
#### REQUEST
```
{
    "email": (email) <string> [required],
    "username": (username) <string> [required],
    "first_name": (first_name) <string> [optional],
    "last_name": (last_name) <string> [optional],
    "age": (1-7) <integer> [optional],
    "gender": (1-2) <integer> [optional],
    "height": (1-4) <integer> [optional],
    "weight": (1-3) <integer> [optional],
    "activity": (1-3) <integer> [optional],
    "dietary_preference": (1-5) <mapped integer> [optional],
    "allergic_food": [
        <mapped integer>,
        <mapped integer>,
        ...
    ] [required]
}
```

#### RESPONSE
```
Same as get response.
```

### (PATCH REQUEST) EDIT USER: http://104.45.142.182/admin/api/users/3/ <--- specify user id
#### REQUEST
```
{
    "first_name": (first_name) <string>,
    "last_name": (last_name) <string>,
    "age": (1-7) <integer>,
    "gender": (1-2) <integer>,
    "height": (1-4) <integer>,
    "weight": (1-3) <integer>,
    "activity": (1-3) <integer>,
    "dietary_preference": (1-5) <mapped integer>,
    "allergic_food": [
        <mapped integer>,
        <mapped integer>,
        ...
    ]
}
```

#### RESPONSE
```
Same as get response,
```

### (DELETE REQUEST) DELETE USER: http://104.45.142.182/admin/api/users/3/ <--- specify user id
#### RESPONSE
```
Same as get response.
```

## ALLERGYMAPPING

### (GET REQUEST): http://104.45.142.182/admin/api/allergymapping/
#### RESPONSE
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "milk": 301 <integer>,
            "egg": 302,
            "peanut": 303,
            "tree_nut": 304,
            "soy": 305,
            "wheat": 306,
            "fish": 307,
            "shellfish": 308,
            "msg_monosodium_glutamate": 309,
            "high_fructose_corn_syrup_hfcs": 310,
            "mustard": 311,
            "celery": 312,
            "sesame": 313,
            "gluten": 314,
            "red_yellow_blue_dye": 315,
            "gluten_free_per_fda": 316,
            "non_gmo_claim": 317
        }
    ]
}
```

## RECOMMENDER

### (GET REQUEST): http://104.45.142.182/admin/api/recommendedfood/?id=5 <--- specify user id
#### RESPONSE
```
{
    "count": (count),
    "next": (url of next page),
    "previous": (url of previous page),
    "results": [
        {
            "recipe_id": "L291833",
            "recipe_name": "DREXEL Orange Juice Fresh",
            "marketing_description": "Orange 100% juice",
            "allergen_attributes": "OrderedDict([('allergen_statement_not_available', None), ('contains_shellfish', 'NO'), ('contains_peanut', 'NO'), ('contains_tree_nuts', 'NO'), ('contains_milk', 'NO'), ('contains_wheat', 'NO'), ('contains_soy', 'NO'), ('contains_eggs', 'NO'), ('contains_fish', 'NO'), ('contains_added_msg', 'UNKNOWN'), ('contains_hfcs', 'UNKNOWN'), ('contains_mustard', 'UNKNOWN'), ('contains_celery', 'UNKNOWN'), ('contains_sesame', 'UNKNOWN'), ('contains_red_yellow_blue_dye', 'UNKNOWN'), ('gluten_free_per_fda', 'UNKNOWN'), ('non_gmo_claim', 'UNKNOWN'), ('contains_gluten', 'YES')])",
            "dietary_attributes": "OrderedDict([('vegan', 'YES'), ('vegetarian', 'YES'), ('kosher', 'YES'), ('halal', 'YES')])"
            "avg_rating": (0-5) <float>
        },
        {
            "recipe_id": "L291879",
            "recipe_name": "DREXEL Apple Juice 46OZ",
            "marketing_description": "Apple 100% juice",
            "allergen_attributes": "OrderedDict([('allergen_statement_not_available', None), ('contains_shellfish', 'NO'), ('contains_peanut', 'NO'), ('contains_tree_nuts', 'NO'), ('contains_milk', 'NO'), ('contains_wheat', 'NO'), ('contains_soy', 'NO'), ('contains_eggs', 'NO'), ('contains_fish', 'NO'), ('contains_added_msg', 'UNKNOWN'), ('contains_hfcs', 'UNKNOWN'), ('contains_mustard', 'UNKNOWN'), ('contains_celery', 'UNKNOWN'), ('contains_sesame', 'UNKNOWN'), ('contains_red_yellow_blue_dye', 'UNKNOWN'), ('gluten_free_per_fda', 'UNKNOWN'), ('non_gmo_claim', 'UNKNOWN'), ('contains_gluten', 'YES')])",
            "dietary_attributes": "OrderedDict([('vegan', 'YES'), ('vegetarian', 'YES'), ('kosher', 'YES'), ('halal', 'YES')])"
            "avg_rating": (0-5) <float>
        },
        ...
}
```

## MEALS

### (GET REQUEST) GET ALL MEALS: http://104.45.142.182/admin/api/meals/?search=L291833 <--- optional (?search=L291833)
Can search for recipe_id or recipe_name
#### RESPONSE
```
{
    "count": 294,
    "next": (url of next page),
    "previous": (url of previous page),
    "results": [
        {
            "recipe_id": "L291833",
            "recipe_name": "DREXEL Orange Juice Fresh",
            "marketing_description": "Orange 100% juice",
            "allergen_attributes": "OrderedDict([('allergen_statement_not_available', None), ('contains_shellfish', 'NO'), ('contains_peanut', 'NO'), ('contains_tree_nuts', 'NO'), ('contains_milk', 'NO'), ('contains_wheat', 'NO'), ('contains_soy', 'NO'), ('contains_eggs', 'NO'), ('contains_fish', 'NO'), ('contains_added_msg', 'UNKNOWN'), ('contains_hfcs', 'UNKNOWN'), ('contains_mustard', 'UNKNOWN'), ('contains_celery', 'UNKNOWN'), ('contains_sesame', 'UNKNOWN'), ('contains_red_yellow_blue_dye', 'UNKNOWN'), ('gluten_free_per_fda', 'UNKNOWN'), ('non_gmo_claim', 'UNKNOWN'), ('contains_gluten', 'YES')])",
            "dietary_attributes": "OrderedDict([('vegan', 'YES'), ('vegetarian', 'YES'), ('kosher', 'YES'), ('halal', 'YES')])"
            "avg_rating": (0-5) <float>
        },
        {
            "recipe_id": "L291879",
            "recipe_name": "DREXEL Apple Juice 46OZ",
            "marketing_description": "Apple 100% juice",
            "allergen_attributes": "OrderedDict([('allergen_statement_not_available', None), ('contains_shellfish', 'NO'), ('contains_peanut', 'NO'), ('contains_tree_nuts', 'NO'), ('contains_milk', 'NO'), ('contains_wheat', 'NO'), ('contains_soy', 'NO'), ('contains_eggs', 'NO'), ('contains_fish', 'NO'), ('contains_added_msg', 'UNKNOWN'), ('contains_hfcs', 'UNKNOWN'), ('contains_mustard', 'UNKNOWN'), ('contains_celery', 'UNKNOWN'), ('contains_sesame', 'UNKNOWN'), ('contains_red_yellow_blue_dye', 'UNKNOWN'), ('gluten_free_per_fda', 'UNKNOWN'), ('non_gmo_claim', 'UNKNOWN'), ('contains_gluten', 'YES')])",
            "dietary_attributes": "OrderedDict([('vegan', 'YES'), ('vegetarian', 'YES'), ('kosher', 'YES'), ('halal', 'YES')])"
            "avg_rating": (0-5) <float>
        },
        ...
}
```

### (GET REQUEST) GET ONE MEAL: http://104.45.142.182/admin/api/meals/L291833/ <--- specify meal id
#### RESPONSE
```
{
    "recipe_id": "L291833",
    "recipe_name": "DREXEL Orange Juice Fresh",
    "marketing_description": "Orange 100% juice",
    "allergen_attributes": "OrderedDict([('allergen_statement_not_available', None), ('contains_shellfish', 'NO'), ('contains_peanut', 'NO'), ('contains_tree_nuts', 'NO'), ('contains_milk', 'NO'), ('contains_wheat', 'NO'), ('contains_soy', 'NO'), ('contains_eggs', 'NO'), ('contains_fish', 'NO'), ('contains_added_msg', 'UNKNOWN'), ('contains_hfcs', 'UNKNOWN'), ('contains_mustard', 'UNKNOWN'), ('contains_celery', 'UNKNOWN'), ('contains_sesame', 'UNKNOWN'), ('contains_red_yellow_blue_dye', 'UNKNOWN'), ('gluten_free_per_fda', 'UNKNOWN'), ('non_gmo_claim', 'UNKNOWN'), ('contains_gluten', 'YES')])",
    "dietary_attributes": "OrderedDict([('vegan', 'YES'), ('vegetarian', 'YES'), ('kosher', 'YES'), ('halal', 'YES')])",
    "avg_rating": (0-5) <float>
}
```

## RATING

### (GET REQUEST) GET ALL RATINGS: http://104.45.142.182/admin/api/rating/
#### RESPONSE
```
{
    "count": (count) <integer>,
    "next": (url of next page),
    "previous": (url of previous page),
    "results": [
        {
            "profile_id": (profile_id) <integer>,
            "recipe_id": (recipe_id) <string>,
            "meal_period": (1-4) <integer>,
            "rating": (rating) <float>
        },
        {
            "profile_id": (profile_id) <integer>,
            "recipe_id": (recipe_id) <string>,
            "meal_period": (1-4) <integer>,
            "rating": (rating) <float>
        },
        ...
}
```

### (GET REQUEST) GET ONE RATING: http://104.45.142.182/admin/api/rating/27/ <--- specify rating id
#### RESPONSE
```
{
    "id": 27 <integer>,
    "profile_id": (profile_id) <integer>,
    "recipe_id": (recipe_id) <string>,
    "rating": (rating) <float>
}
```

### (POST REQUEST): http://104.45.142.182/admin/api/rating/
#### REQUEST
```
{
    "profile_id": (profile_id) <integer>,
    "recipe_id": (recipe_id) <string>,
    "rating": (rating) <float>
}
```

#### RESPONSE
```
Same as get request.
```

### (DELETE REQUEST): http://104.45.142.182/admin/api/rating/27/ <--- specify rating id
#### RESPONSE
```
Same as get request.
```

## CUSTOM_RECIPE

### (GET REQUEST) GET ALL CUSTOM_RECIPE: http://104.45.142.182/admin/api/customrecipe/
#### RESPONSE
```
{
    "count": (count) <integer>,
    "next": (url of next page),
    "previous": (url of previous page),
    "results": [
        {
            "id": (id) <integer>,
            "recipe_name": (recipe_name) <string>,
            "recipe_description": (recipe_description) <string>,
            "preparation_time": (preparation_time) <string>,
            "number_of_servings": (number_of_servings) <float>,
            "calories_per_serving": (calories_per_serving) <float>
        },
        {
            "id": (id) <integer>,
            "recipe_name": (recipe_name) <string>,
            "recipe_description": (recipe_description) <string>,
            "preparation_time": (preparation_time) <string>,
            "number_of_servings": (number_of_servings) <float>,
            "calories_per_serving": (calories_per_serving) <float>
        },
        ...
    ]
}
```

### (GET REQUEST) GET ONE CUSTOMRECIPE: http://104.45.142.182/admin/api/customrecipe/27/ <--- specify id
#### RESPONSE
```
{
    "id": 27 <integer>,
    "recipe_name": (recipe_name) <string>,
    "recipe_description": (recipe_description) <string>,
    "preparation_time": (preparation_time) <string>,
    "number_of_servings": (number_of_servings) <float>,
    "calories_per_serving": (calories_per_serving) <float>
}
```

### (POST REQUEST): http://104.45.142.182/admin/api/customrecipe/
#### REQUEST
```
{
    "recipe_name": (recipe_name) <string>,
    "recipe_description": (recipe_description) <string>,
    "preparation_time": (preparation_time) <string>,
    "number_of_servings": (number_of_servings) <float>,
    "calories_per_serving": (calories_per_serving) <float>
}
```

#### RESPONSE
```
Same as get request.
```

### (PATCH REQUEST): http://104.45.142.182/admin/api/customrecipe/27/ <--- specify id
#### REQUEST
```
{
    "recipe_name": (recipe_name) <string> [required],
    "recipe_description": (recipe_description) <string> [optional],
    "preparation_time": (preparation_time) <string> [optional],
    "number_of_servings": (number_of_servings) <float> [required],
    "calories_per_serving": (calories_per_serving) <float> [required]
}
```

#### RESPONSE
```
Same as get request.
```

### (DELETE REQUEST): http://104.45.142.182/admin/api/customrecipe/27/ <--- specify id
#### RESPONSE
```
Same as get request.
```

## DIARY

### (GET REQUEST) GET ENTRIES: http://104.45.142.182/admin/api/diary/?profile_id=5 <--- optional (?profile_id=5)

#### RESPONSE
```
{
    "count": (count) <integer>,
    "next": (url of next page),
    "previous": (url of previous page),
    "results": [
        {
            "id": (id) <integer>,
            "timestamp_millis": (timestamp_millis) <integer>,
            "profile_id": (profile_id) <integer>,
            "meal_period": (1-4) <integer>,
            "is_custom_recipe": <boolean>,
            "custom_recipe": [] <list of strings>,
            "meals": [] <list of strings>
        },
        {
            "id": (id) <integer>,
            "timestamp_millis": (timestamp_millis) <integer>,
            "profile_id": (profile_id) <integer>,
            "meal_period": (1-4) <integer>,
            "is_custom_recipe": <boolean>,
            "custom_recipe": [] <list of strings>,
            "meals": [] <list of strings>
        },
        ...
}
```

### (GET REQUEST) GET ONE ENTRY: http://104.45.142.182/admin/api/diary/27/ <--- specify id
#### RESPONSE
```
{
    "id": 27,
    "timestamp_millis": (timestamp_millis) <integer>,
    "profile_id": (profile_id) <integer>,
    "meal_period": (1-4) <integer> ,
    "is_custom_recipe": <boolean>,
    "custom_recipe": [] <list of strings>,
    "meals": [] <list of strings>
}
```

### (POST REQUEST): http://104.45.142.1824/admin/api/diary/
#### REQUEST
```
{
    "timestamp_millis": (timestamp_millis) <integer>,
    "profile_id": (profile_id) <integer>,
    "meal_period": (1-4) <integer> ,
    "is_custom_recipe": <boolean>,
    "custom_recipe": [] <list of strings>,
    "meals": [] <list of strings>
}
```

#### RESPONSE
```
Same as get request.
```

### (PATCH REQUEST): http://104.45.142.182/admin/api/diary/27/ <--- specify id
#### REQUEST
```
{
    "timestamp_millis": (timestamp_millis) <integer> [optional],
    "profile_id": (profile_id) <integer> [required],
    "meal_period": (1-4) <integer> [required],
    "is_custom_recipe": <boolean> [optional],
    "custom_recipe": [] <list of strings> [required empty list],
    "meals": [] <list of strings> [required empty list]
}
```

#### RESPONSE
```
Same as get request.
```

### (DELETE REQUEST): http://104.45.142.182/admin/api/diary/27/ <--- specify id
#### RESPONSE
```
Same as get request.
```

Note: These APIs require trailing backlash except for RECOMMENDER
