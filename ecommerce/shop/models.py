from django.db import models

# Create your models here.
class Categories(models.Model):
    image=models.ImageField(upload_to="images")
    name=models.CharField(max_length=30)
    description=models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to="products")
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True) #one time
    updated=models.DateTimeField(auto_now=True) #change every time we update record
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class Users(models.Model):
#     name=models.CharField(max_length=20)
#     age=models.IntegerField()
#     place= models.CharField(max_length=20)
#     gender=models.CharField(max_length=20)

