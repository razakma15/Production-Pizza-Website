from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractUser

"""Creation of Meal model which stores information of the attributes
of all food items to be used by the Menu.html page"""

class Meal(models.Model):
    title = models.CharField(max_length=30,default="null")
    description = models.CharField(max_length=1000,default="null")
    type = models.CharField(max_length=15,default="Main")
    price = models.IntegerField(default=0)
    image = models.CharField(max_length=250,default="null")
    def __str__(self):
        return str(self.title)

"""Creation of CustomUser which inherets the class AbstractUser to create a custom user model
based on the the included django user class which means a reduction in the work needed and we can
 also use powerful features of the included model such as password encryption and calling request attributes"""

class CustomUser(AbstractUser):
    basket_quantity = models.IntegerField(default=0)
# link to create many to many relational database which allows each user to have their specific choices of food.
    meal = models.ManyToManyField(Meal)
    def __str__(self):
        return str(self.username)

""" MAJOR FLAW - each food objects needs its own quantity as this leads to major logic and security
issues. This hasnt been fixed yet due to time restraints and the project fufilling its purpose
to increase my profiencey in django"""
