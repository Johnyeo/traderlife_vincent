from django.db import models

# Create your models here.

class Game(models.Model):
    player = models.CharField(max_length=100)
    gameround = models.IntegerField()
    flag = models.CharField(max_length=1)
    create_time = models.DateTimeField(auto_now=True)

class Market_goods(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=24, decimal_places=2)
    quality = models.IntegerField()
    count = models.IntegerField()
    status = models.BooleanField()
    flag = models.CharField(max_length=1)
    create_time = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class My_goods(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=24, decimal_places=2)
    quality = models.IntegerField()
    count = models.IntegerField()
    status = models.BooleanField()
    username = models.CharField(max_length=100)
    flag = models.CharField(max_length=1)
    create_time = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=200)
    gameid = models.ForeignKey(Game)  # 游戏场次的id
    gameround = models.IntegerField()   # 该场次，游戏回合的id

class Event(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000)
    type = models.CharField(max_length=1)
    status = models.BooleanField()
    flag = models.CharField(max_length=1)
    create_time = models.DateTimeField(auto_now=True)



class meta:
    unique_together = ()

