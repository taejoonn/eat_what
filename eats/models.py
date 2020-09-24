from django.db import models

# Create your models here.

class Order(models.Model):
    item = models.CharField(verbose_name='item', max_length=30, help_text='food')

    def __str__(self):
        return self.item


class Rating(models.Model):
    id = models.IntegerField(verbose_name='id', primary_key=True)
    order = models.ManyToManyField(Order)
    rate = models.SmallIntegerField(verbose_name='rate')

    def __str__(self):
        return self.id


class Result(models.Model):
    id = models.IntegerField(verbose_name='id', primary_key=True)
    name = models.CharField(verbose_name='name', max_length=30, help_text='Name of resulting restaurant')
    address = models.CharField(verbose_name='address', max_length=255, help_text='Address of resulting restaurant')
    date = models.DateTimeField(verbose_name='date')
    lat = models.FloatField(verbose_name='lat')
    long = models.FloatField(verbose_name='long')
    radius = models.FloatField(verbose_name='radius')
    phone = models.CharField(verbose_name='phone', max_length=11)
    url = models.CharField(verbose_name='url', max_length=255)
    rating = models.OneToOneField(
        Rating,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class User(models.Model):
    """ User model to save history/preferences """
    username = models.CharField(primary_key=True , max_length=20)
    results = models.ManyToManyField(
        Result,
    )

    def __str__(self):
        return self.username
