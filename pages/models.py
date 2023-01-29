from django.db import models
import datetime

# Create your models here.
class Poll(models.Model):
        name = models.CharField(max_length=120,default='')
        question = models.TextField()
        option_one = models.CharField(max_length=60)
        option_two = models.CharField(max_length=60)
        option_three = models.CharField(max_length=60)
        option_four = models.CharField(max_length=60)
        option_one_count = models.IntegerField(default=0)
        option_two_count = models.IntegerField(default=0)
        option_three_count = models.IntegerField(default=0)
        option_four_count = models.IntegerField(default=0)
        date =models.DateTimeField(auto_now=True)

        def time(self):
            return self.date
        
        def __str__(self):
              return self.question
        
        def total(self):
             
             return self.option_one_count + self.option_two_count + self.option_three_count + self.option_four_count


class User(models.Model):
        name  = models.CharField(max_length=50)
        email = models.EmailField(max_length=100)
        password = models.CharField(max_length=150)
        

      
        
        def  __str__(self):
              return self.name

               
