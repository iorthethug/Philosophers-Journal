from django.db import models

# Create your models here.
#I think I dont need all these fields, I will remove some of them
class Philosopher(models.Model): # Philosopher model
    name = models.CharField(max_length=100)
    bio = models.TextField()
    school_of_thought = models.CharField(max_length=100)
    core_ideas = models.JSONField(default=list)
    tone = models.CharField(max_length=100)
    works = models.JSONField(default=list)
    era = models.CharField(max_length=50)
    quotes = models.JSONField(default=list)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class UserInput(models.Model): # UserInput model
    user_text = models.TextField()
    sentiment = models.CharField(max_length=50)
    keywords = models.TextField()
    matched_philosopher = models.ForeignKey(Philosopher, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Input at {self.created_at}"