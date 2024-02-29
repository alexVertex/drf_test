from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Manufacture(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, related_name='manufactures', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manufacture = models.ForeignKey(Manufacture, related_name='cars', on_delete=models.CASCADE)
    dateStartProduce = models.DateField()
    dateStopProduce = models.DateField()

    def __str__(self):
        return self.name


class Commentary(models.Model):
    email = models.EmailField()
    car = models.ForeignKey(Car, related_name='commentarys', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    commentaryData = models.TextField(blank=True)

    def __str__(self):
        return str(self.email) + " (" + str(self.date) + "): " + str(self.commentaryData)
