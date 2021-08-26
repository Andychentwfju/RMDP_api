from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from serializers import *


# Create your views here.

# Create your views here.
@api_view(['POST'])
def getCountryCode(request):
    offset = int(request.data['params']['skip'])
    items_per_page = int(request.data['params']['limit'])
    countryList = country_code.objects.skip(offset).limit(items_per_page)
    result = countrySerializer(countryList, many=True)
    response = JsonResponse(result.data, safe=False)
    return response


# Create your views here.
@api_view(['POST'])
def getCities(request):
    offset = int(request.data['params']['skip'])
    items_per_page = int(request.data['params']['limit'])
    cityList = all_cities.objects.skip(offset).limit(items_per_page)
    result = CitySerializer(cityList, many=True)
    response = JsonResponse(result.data, safe=False)
    return response


@api_view(['GET'])
def getAllCities(request):
    cityList = all_cities.objects.all()
    result = CitySerializer(cityList, many=True)
    response = JsonResponse(result.data, safe=False)
    return response


@api_view(['GET'])
def getAllCountryCode(request):
    countryList = country_code.objects.all()
    result = countrySerializer(countryList, many=True)
    response = JsonResponse(result.data, safe=False)
    return response