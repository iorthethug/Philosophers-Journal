from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

from .models import Philosopher
from .serializers import PhilosopherSerializer

# Create your views here.

def analyze_user_input(user_text): #2 returns keywords and sentiment maybe the transformer here? NLKT
    return None

def match_philosopher(user_text): #3 returns matched philosopher
    return None

def user_input(request): #1 returns the response
    return None