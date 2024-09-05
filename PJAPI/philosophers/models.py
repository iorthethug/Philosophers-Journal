from django.db import models

# Create your models here.

class Philosopher(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    birth_year = models.IntegerField()
    keywords = models.TextField()
    works = models.TextField()
    philosophical_school = models.CharField(max_length=100)

    class Meta:
        unique_together = ('name', 'birth_year')

    def __str__(self):
        return self.name