from django.contrib import admin
from .models import Philosopher, UserInput

class PhilosopherAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_of_thought', 'era')
    search_fields = ('name', 'school_of_thought', 'core_ideas', 'tone','works', 'era' , 'quotes')
    list_filter = ('school_of_thought', 'era')

class UserInputAdmin(admin.ModelAdmin):
    list_display = ('user_text', 'sentiment', 'created_at', 'matched_philosopher')
    search_fields = ('user_text', 'sentiment', 'keywords')
    list_filter = ('sentiment', 'created_at')

admin.site.register(Philosopher, PhilosopherAdmin)
admin.site.register(UserInput, UserInputAdmin)