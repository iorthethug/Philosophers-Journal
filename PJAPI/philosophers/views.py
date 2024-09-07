from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

from .models import Philosopher
from .serializers import PhilosopherSerializer

# Create your views here.

def analyze_user_input(user_text): # returns keywords and sentiment
    return None

def match_philosopher(user_text): # returns matched philosopher
    return None

def user_input(request): # returns the response
    return None