from django.db import models

# Create your models here.

class Philosopher(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    school_of_thought = models.CharField(max_length=100)
    core_ideas = models.JSONField(default=list)
    tone = models.CharField(max_length=100)
    works = models.JSONField(default=list) 
    era = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class UserInput(models.Model):
    user_text = models.TextField()
    sentiment = models.CharField(max_length=50)
    keywords = models.TextField()
    matched_philosopher = models.ForeignKey(Philosopher, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Input at {self.created_at}"