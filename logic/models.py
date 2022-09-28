from django.db import models
from django.contrib.auth.models import User
from django import forms

class Vehicle_Model(models.Model):
    length = models.IntegerField("Truck length")
    width = models.IntegerField("Truck width")
    height = models.IntegerField("Truck height", blank = True, null = True)

class Boxes_Model(models.Model):
    length = models.IntegerField("Box length")
    width = models.IntegerField("Box width")
    height = models.IntegerField("Box height", blank = True, null = True)