from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData,  user = None):
        errors = {}

        if len(postData['name']) < 3 :
            errors["name"] = "Name should be at least 3 characters "


        if len(postData['username']) < 3:
            errors["username"] =  "userName should be at least 3 characters "

        if len(postData['password']) < 3:
            errors["password"] =  "password should be at least 8 characters "

        if  postData['password'] != postData['confirem-password']:
            errors["password"] =  "Passwords do not match"    


        return errors

class ListwishManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['item']) < 3 :
            errors["item"] = "item should be at least 3 characters "

        if len(postData['item']) == " " :
            errors["item"] = "item should be at least 3 characters "    
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    password_confirem = models.CharField(max_length=255, blank=True,  null=True,)
    data_hired= models.DateTimeField(blank=True, null=True)
    objects = UserManager()



class Listwish(models.Model):
    userId = models.ManyToManyField(User, related_name="itemwish")
    user_name = models.ForeignKey(User, blank=True,  null=True, related_name="userNames", on_delete = models.CASCADE)
    item = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = ListwishManager()

