from django.db import models

class Vehicle_Model(models.Model):
    length = models.IntegerField("Truck length")
    width = models.IntegerField("Truck width")

class Boxes_Model(models.Model):
    length = models.IntegerField("Box length")
    width = models.IntegerField("Box width")