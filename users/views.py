'''
ViewSets are essentially just a type of class based view, that doesn't provide
any method handlers, such as `get()`, `post()`, etc... but instead has actions,
such as `list()`, `retrieve()`, `create()`, etc...

Actions are only bound to methods at the point of instantiating the views.
    user_list = UserViewSet.as_view({'get': 'list'})
    user_detail = UserViewSet.as_view({'get': 'retrieve'})

Typically, rather than instantiate views from viewsets directly, you'll
register the viewset with a router and let the URL conf be determined
automatically.
    router = DefaultRouter()
    router.register(r'users', UserViewSet, 'user')
    urlpatterns = router.urls

https://github.com/encode/django-rest-framework/blob/master/rest_framework/viewsets.py
https://www.django-rest-framework.org/api-guide/viewsets/

https://github.com/encode/django-rest-framework/blob/master/rest_framework/views.py
https://www.django-rest-framework.org/api-guide/generic-views/
https://docs.djangoproject.com/en/3.0/topics/class-based-views/
https://docs.djangoproject.com/en/3.0/ref/views/
'''
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg

from rest_framework import pagination
from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
# from rest_framework.parsers import JSONParser, ParseError

from . import models
from . import serializers

from CDS import cds_cal #, new_recipes, service_menu_items_flat, service_recipe_nutrition
import json

from rest_framework import filters
import ast 

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    #Fields expected from JSON POST
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    #Check if username or email already exists
    #True: Return error
    #False: Return created user with token
    if models.CustomUser.objects.filter(username=username).exists():
        return Response({"code": 1, "error": "Username is already in use"})
    elif models.CustomUser.objects.filter(email=email).exists():
        return Response({"code": 2, "error": "Email is already in use"})
    else:
        user = models.CustomUser.objects.create_user(username, email, password)
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        userquery = models.CustomUser.objects.filter(username=username)
        return Response({'token': token.key, 'user': userquery.values("id", "username", "email")[0]},
                    status=HTTP_200_OK)
    
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    #Fields expected from JSON POST
    username = request.data.get("username")
    password = request.data.get("password")

    #Check if any of the fields are empty
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    #Check if user is in database
    if not user:
        return Response({'status': False, 'token': None, 'user': None},
                        status=HTTP_200_OK)

    #Return token and profile information
    token, _ = Token.objects.get_or_create(user=user)
    userquery = models.CustomUser.objects.filter(username=username)
    # if userquery.values("first_name")[0]["first_name"] == '':
    for lists in userquery.values("id", "username", "email",
                    "first_name", "last_name", "age", "gender", "height", "weight", "activity",
                    "dietary_preference", "allergic_food"):
        for values in lists.values():
            if values is None:
                #Check if user has missing information  
                return Response({"code": 3, "error": "Missing profile information", 'status': True, 'token': token.key, 
                    'user': userquery.values("id", "username", "email",
                    "first_name", "last_name", "age", "gender", "height", "weight", "activity",
                    "dietary_preference", "allergic_food")[0]})
    return Response({'status': True, 'token': token.key, 'user': userquery.values("id", "username", "email",
                    "first_name", "last_name", "age", "gender", "height", "weight", "activity",
                    "dietary_preference", "allergic_food")[0]},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logout(request):
    #Fields expected from JSON POST
    user_id = request.data.get("user_id")
    token = request.data.get("token")

    #Delete token once logged out
    Token.objects.filter(user=user_id, key=token).delete()
    data = {'success': 'Sucessfully logged out'}
    return Response(data=data, status=HTTP_200_OK)

class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj == request.user
        else:
            return False

        if request.method == SAFE_METHODS:
            return True

class UserViewSet(mixins.CreateModelMixin, 
                mixins.RetrieveModelMixin, 
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    queryset = models.CustomUser.objects.all().order_by('id')
    serializer_class = serializers.UserSerializer

class AllergyMappingViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.AllergyMapping.objects.all().order_by('id')
    serializer_class = serializers.AllergyMappingSerializer

class RecommendedFoodViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.RecommendedFood.objects.all().order_by('recipe_id')
    ratingquery = models.Rating.objects.all()
    serializer_class = serializers.RecommendedFoodSerializer

    # #Search functionality for recipes
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['recipe_id', 'recipe_name']

    def get_queryset(self):
        #Queryset for RecommendedFood
        queryset = self.queryset
        ratingquery = self.ratingquery

        #Queryset for CustomUser to get specific user with given ID
        userquery = models.CustomUser.objects.filter(id=self.request.query_params.get('id'))

        #Mapping for CDS
        gender_convert = {1: 'M', 2: 'F'}
        age_convert = {1:"1-3", 2:"4-8", 3:"9-13", 4:"14-18", 5: "19-30", 6: "31-50", 7: "51-99"}
        lifestyle_convert = {1:'Sedentary', 2:'Moderate', 3:'Active'}
        allergens =  models.AllergyMapping.objects.all().values()
        dietary = ['halal', 'kosher', 'vegan', 'vegetarian']
        mealstype_convert = {1:"vegan", 2:"vegetarian", 3:"halal", 4:"kosher", 5:"meat"}


        for n in userquery.values("allergic_food", "dietary_preference", 'gender', 'age', 'activity'):
            # allergy_list = n['allergic_food']
            # diet = (mealstype_convert[n['dietary_preference']] if n['dietary_preference'] else None)
            # gender = gender_convert[n["gender"]]
            # age = age_convert[n["age"]]
            # lifestyle = lifestyle_convert[n["activity"]]
            gender = (gender_convert[n["gender"]] if n['gender'] != None else 'F')
            age = (age_convert[n["age"]] if n['age'] != None else '19-30')
            lifestyle = (lifestyle_convert[n["activity"]] if n['activity'] != (None and 4) else 'Moderate')
            allergy_list = n['allergic_food']
            diet = (mealstype_convert[n['dietary_preference']] if n['dietary_preference'] else None)

        recipe_query = queryset
        # recipe_query = models.RecommendedFood.objects.all()
        service_recipe_nutrition = []
        for item in recipe_query.values():
            # item['dietary_attributes'] = dict(ast.literal_eval(item['dietary_attributes']))
            # item['allergen_attributes'] = dict(ast.literal_eval(item['allergen_attributes']))
            # item['primary_attributes'] = dict(ast.literal_eval(item['primary_attributes'][12:-1]))
            # item['secondary_attributes'] = dict(ast.literal_eval(item['secondary_attributes'][12:-1]))
            for it in item['primary_attributes']:
                if item['primary_attributes'][it] == None:
                    item['primary_attributes'][it] = 0
            service_recipe_nutrition.append(item)

        service_menu_items_flat =  models.ServiceMenuitemsFlat.objects.all().values()
        hei_file =  models.NewRecipe.objects.all().values()
        # service_menu_items_flat = []
        # for item in flat_query.values():
        #     service_menu_items_flat.append(item)
        # with open("CDS/service_recipe_nutrition.json",'r') as file:
        #     service_recipe_nutrition = json.load(file)

        # with open("CDS/service_menu_items_flat.json",'r') as file:
        #     service_menu_items_flat = json.load(file)

        # with open("CDS/new_recipes_0-1.json",'r') as file:
        #     hei_file = json.load(file)
        
        time_of_meal = 'Lunch'

        computed_cds = cds_cal.cds_cal(gender,age,lifestyle,time_of_meal, service_recipe_nutrition, service_menu_items_flat, hei_file)

        # recommend = [] # recommended recipe holder
        # for item in computed_cds[:50]:
        #     for recipe in queryset.values():
        #         if item['recipe_id'] == recipe['recipe_id']:
        #             recommend.append(recipe)

        recommend1 = [] # recommended recipe holder
        ind1 = '_' 
        
        trans = []
        for num in allergy_list:
            for lists in allergens: #.items():
                for item, number in lists.items():   
                    if number == num:
                        trans.append(item)
        # print(diet)
        # allerta = dict(ast.literal_eval(recipe1['allergen_attributes'][12:-1]))
        # dieta = dict(ast.literal_eval(recipe1['dietary_attributes'][12:-1]))
        #     allerta = dict(ast.literal_eval(recipe1['allergen_attributes'][12:-1]))
        #     print(dieta['halal'])

        for recipe1 in computed_cds: # for every recipe from the json file
            ind = False # set indicator to False
            # dieta = recipe1['dietary_attributes']
            dieta = dict(ast.literal_eval(recipe1['dietary_attributes'][12:-1]))
            allerta = recipe1['allergen_attributes']
            if diet is not None:
                if dieta[diet] == 'NO' or dieta[diet] == None or  dieta[diet] == 'UNKNOWN':
                    ind = True # set the indicator to true and break
                    # print(ind)
                    continue
            for allergent in allerta: # for every allergent in the recipe
                for user_allergy in trans: # loop through for each individual user provided allergent
                    if ind1 + str(user_allergy) in allergent: # check if the user_allergent matches the allergent that we are currently looping through
                        if (allerta[allergent] == 'YES'): # if the user provided allergent is actually an allergent in the recipe
                            ind = True # set the indicator to true and break
                            break
                if ind: # if the indicator is True, break the loop
                    break
            if not ind: # add the recipe to the recommender holder if the indicator is set to False.
                # print('check')
                recommend1.append(recipe1)

        # print(recommend1)
        for n in recommend1:
            avg_rating = None
            # Get all ratings for each recipe
            rating = ratingquery.filter(recipe_id=n['recipe_id'])
            # print(n['recipe_id'], rating)
            # print(n['recipe_id'])
            #Set avg_rating to aggregated avg of ratings
            if rating:                        
                avg_rating = rating.aggregate(Avg("rating"))['rating__avg']
                avg_rating = round(avg_rating,1)
            n['avg_rating'] = avg_rating

        # print(ratingquery.filter(recipe_id="M14894"))


        return recommend1 #queryset.filter(recipe_id__in=recommend1)


class MealsViewSet(viewsets.ModelViewSet):
    queryset = models.Meals.objects.all().order_by('recipe_id')
    ratingquery = models.Rating.objects.all()
    serializer_class = serializers.MealsSerializer

    #Search functionality for recipes
    filter_backends = [filters.SearchFilter]
    search_fields = ['recipe_id', 'recipe_name']

    def get_queryset(self):
        queryset = self.queryset
        ratingquery = self.ratingquery

        #Get ALL
        if self.action == 'list':
            #Get current page
            # page = self.request.GET.get('page')
            # if page != None:
            #     page = int(page)
            # if page == None or search:
            for n in queryset:
                filtered_query = ratingquery.filter(recipe_id=n.recipe_id)
                if filtered_query:
                    avg_rating = filtered_query.aggregate(Avg("rating"))['rating__avg']
                    queryset.filter(recipe_id=n.recipe_id).update(avg_rating=round(avg_rating,1))
        
        #Get specific food
        if self.action == 'retrieve':
            filtered_query = ratingquery.filter(recipe_id=self.kwargs['pk'])
            if filtered_query:
                avg_rating = filtered_query.aggregate(Avg("rating"))['rating__avg']
                queryset.filter(recipe_id=self.kwargs['pk']).update(avg_rating=round(avg_rating,1))
        return queryset

class RatingViewSet(viewsets.ModelViewSet):
    queryset = models.Rating.objects.all()
    serializer_class = serializers.RatingSerializer

    #Get ratings per user
    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('profile_id') is not None:
            queryset = self.queryset.filter(profile_id=self.request.query_params.get('profile_id'))
            return queryset
        return queryset

class CustomRecipeViewSet(viewsets.ModelViewSet):
    queryset = models.CustomRecipe.objects.all()
    serializer_class = serializers.CustomRecipeSerializer

class DiaryViewSet(viewsets.ModelViewSet):
    queryset = models.Diary.objects.all()
    serializer_class = serializers.DiaryEntriesSerializer
    # pagination.PageNumberPagination.page_size = 1000

    #Get diary per user
    def get_queryset(self):
        queryset = self.queryset

        if self.request.query_params.get('profile_id') is not None:
            queryset = self.queryset.filter(profile_id=self.request.query_params.get('profile_id'))
            return queryset
        return queryset







class UserInformationViewSet(viewsets.ModelViewSet):
    queryset = models.UserInformation.objects.all().order_by('id')
    serializer_class = serializers.UserInformationSerializer

# @login_required
# def profile(request):
#     context={
#     'id': request.user.id,
#     'username':request.user.username,
#     'email':request.user.email,
#     'first_name':request.user.first_name,
#     'last_name':request.user.last_name,
#     'age':request.user.age,
#     'gender':request.user.gender,
#     'height':request.user.height,
#     'weight':request.user.weight,
#     'activity':request.user.activity,
#     'allergic_food':request.user.allergic_food
#     }
#     return render(request, 'profile.html',context)

    # def get_read_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return OrderDetailSerializer

    # get_write_serializer_class
    
    # def get_permissions(self):
    #     if self.action == 'list':
    #         self.permission_classes = [IsSuperUser, ]
    #     elif self.action == 'retrieve':
    #         self.permission_classes = [IsUser]
    #     return super(self.__class__, self).get_permissions()

    # def list(self, request):
    #     queryset = CustomUser.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     parsed = serializer.data
    #     parsed = list(parsed[0].items())[0:][0]
    #     key = parsed[0]

    #     value = parsed[1][1:-1].split(', ')
    #     value = [int(i) for i in value]
        
    #     # value = parsed[1][1:-1].replace("'", "" )
    #     # value = list(value.split(', '))
    #     print({key:value})
        
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = Allergies_List.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = Allergies_ListSerializer(user)
    #     print("HEHE",Response(serializer.data))
    #     return Response(serializer.data)

# @csrf_exempt
# def allergies_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         allergies = Allergies_List.objects.all()
#         serializer = Allergies_ListSerializer(allergies, many=True)
#         return JsonResponse(serializer.data, safe=False)

# @csrf_exempt
# def allergies_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         allergies = Allergies_List.objects.get(pk=pk)
#     except Allergies_List.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = Allergies_ListSerializer(allergies)
#         return JsonResponse(serializer.data)

# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer



