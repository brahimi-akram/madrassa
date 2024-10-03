from django.db import models
class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=10)


    def __str__(self):
        return f'{self.name}'
    
class Level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

class Teacher(models.Model):
    name = models.CharField(max_length=60)


class Student(models.Model):
    num = models.IntegerField(unique=True,null=True,blank=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    level = models.ForeignKey("Level",on_delete=models.SET_NULL,null=True,related_name='level_student')
    date_birth = models.DateField()
    adress = models.CharField(max_length=60)
    level_year = models.CharField(max_length=60)
    situation = models.CharField(max_length=40,null=True,blank=True)
    confirmed = models.BooleanField()
    parent = models.ForeignKey("parent",on_delete=models.SET_NULL,null=True ,related_name='children')
    teacher = models.ForeignKey("teacher",on_delete=models.SET_NULL,null=True,blank=True,related_name = 'teacher_student')


    def __str__(self):
        return f'{self.first_name}-{self.last_name} {self.level}'
        
