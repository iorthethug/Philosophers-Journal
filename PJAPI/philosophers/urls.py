from django.urls import path
from .views import user_input_view

urlpatterns = [
    path('', user_input_view, name='user_input'),
]