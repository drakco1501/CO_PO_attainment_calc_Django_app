from django.db import models 
from django.contrib.auth.hashers import make_password


# Create your models here.
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new object
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject_name}"


class NumberOfCO(models.Model):
    subject_name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    num_co_value = models.PositiveIntegerField(default=0)  # Initial value is 0

    def __str__(self):
        return f"{self.subject_name}: {self.num_co_value}"
    
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=255, null=False)
    roll_number = models.CharField(max_length=255, unique=True)  # CharField as primary key

    def __str__(self):
        return f"{self.student_name} ({self.roll_number})"
    
class Marks(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255, null=False)
    student_name = models.CharField(max_length=255, null=False)
    roll_number = models.CharField(max_length=255, null=False)
    IA1_1a = models.PositiveIntegerField(default=0)
    IA1_1b = models.PositiveIntegerField(default=0)
    IA1_2a = models.PositiveIntegerField(default=0)
    IA1_2b = models.PositiveIntegerField(default=0)
    IA2_1a = models.PositiveIntegerField(default=0)
    IA2_1b = models.PositiveIntegerField(default=0)
    IA2_2a = models.PositiveIntegerField(default=0)
    IA2_2b = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.subject_name}({self.roll_number})"
    
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255, null=False, unique=True)
    IA1_1a_que = models.CharField(max_length=255, null=True)
    IA1_1a_co_val = models.PositiveIntegerField(default=0)
    IA1_1b_que = models.CharField(max_length=255, null=True)
    IA1_1b_co_val = models.PositiveIntegerField(default=0)
    IA1_2a_que = models.CharField(max_length=255, null=True)
    IA1_2a_co_val = models.PositiveIntegerField(default=0)
    IA1_2b_que = models.CharField(max_length=255, null=True)
    IA1_2b_co_val = models.PositiveIntegerField(default=0)
    IA2_1a_que = models.CharField(max_length=255, null=True)
    IA2_1a_co_val = models.PositiveIntegerField(default=0)
    IA2_1b_que = models.CharField(max_length=255, null=True)
    IA2_1b_co_val = models.PositiveIntegerField(default=0)
    IA2_2a_que = models.CharField(max_length=255, null=True)
    IA2_2a_co_val = models.PositiveIntegerField(default=0)
    IA2_2b_que = models.CharField(max_length=255, null=True)
    IA2_2b_co_val = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.subject_name}"
    

class CO1(models.Model):
    subject_name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    po1 = models.PositiveIntegerField(default=0)  # Initial value is 0
    po2 = models.PositiveIntegerField(default=0)  
    po3 = models.PositiveIntegerField(default=0)  
    po4 = models.PositiveIntegerField(default=0)  
    po5 = models.PositiveIntegerField(default=0)  
    po6 = models.PositiveIntegerField(default=0)  
    po7 = models.PositiveIntegerField(default=0)  
    po8 = models.PositiveIntegerField(default=0)  
    po9 = models.PositiveIntegerField(default=0)  
    po10 = models.PositiveIntegerField(default=0)  
    po11 = models.PositiveIntegerField(default=0)  
    po12 = models.PositiveIntegerField(default=0)  
    pso1 = models.PositiveIntegerField(default=0)  
    pso2 = models.PositiveIntegerField(default=0)  
    pso3 = models.PositiveIntegerField(default=0)  
    pso4 = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.subject_name}"
    
class CO2(models.Model):
    subject_name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    po1 = models.PositiveIntegerField(default=0)  # Initial value is 0
    po2 = models.PositiveIntegerField(default=0)  
    po3 = models.PositiveIntegerField(default=0)  
    po4 = models.PositiveIntegerField(default=0)  
    po5 = models.PositiveIntegerField(default=0)  
    po6 = models.PositiveIntegerField(default=0)  
    po7 = models.PositiveIntegerField(default=0)  
    po8 = models.PositiveIntegerField(default=0)  
    po9 = models.PositiveIntegerField(default=0)  
    po10 = models.PositiveIntegerField(default=0)  
    po11 = models.PositiveIntegerField(default=0)  
    po12 = models.PositiveIntegerField(default=0)  
    pso1 = models.PositiveIntegerField(default=0)  
    pso2 = models.PositiveIntegerField(default=0)  
    pso3 = models.PositiveIntegerField(default=0)  
    pso4 = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.subject_name}"
    
class CO3(models.Model):
    subject_name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    po1 = models.PositiveIntegerField(default=0)  # Initial value is 0
    po2 = models.PositiveIntegerField(default=0)  
    po3 = models.PositiveIntegerField(default=0)  
    po4 = models.PositiveIntegerField(default=0)  
    po5 = models.PositiveIntegerField(default=0)  
    po6 = models.PositiveIntegerField(default=0)  
    po7 = models.PositiveIntegerField(default=0)  
    po8 = models.PositiveIntegerField(default=0)  
    po9 = models.PositiveIntegerField(default=0)  
    po10 = models.PositiveIntegerField(default=0)  
    po11 = models.PositiveIntegerField(default=0)  
    po12 = models.PositiveIntegerField(default=0)  
    pso1 = models.PositiveIntegerField(default=0)  
    pso2 = models.PositiveIntegerField(default=0)  
    pso3 = models.PositiveIntegerField(default=0)  
    pso4 = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.subject_name}"
    
class CO4(models.Model):
    subject_name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    po1 = models.PositiveIntegerField(default=0)  # Initial value is 0
    po2 = models.PositiveIntegerField(default=0)  
    po3 = models.PositiveIntegerField(default=0)  
    po4 = models.PositiveIntegerField(default=0)  
    po5 = models.PositiveIntegerField(default=0)  
    po6 = models.PositiveIntegerField(default=0)  
    po7 = models.PositiveIntegerField(default=0)  
    po8 = models.PositiveIntegerField(default=0)  
    po9 = models.PositiveIntegerField(default=0)  
    po10 = models.PositiveIntegerField(default=0)  
    po11 = models.PositiveIntegerField(default=0)  
    po12 = models.PositiveIntegerField(default=0)  
    pso1 = models.PositiveIntegerField(default=0)  
    pso2 = models.PositiveIntegerField(default=0)  
    pso3 = models.PositiveIntegerField(default=0)  
    pso4 = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.subject_name}"

class CO5(models.Model):
    subject_name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    po1 = models.PositiveIntegerField(default=0)  # Initial value is 0
    po2 = models.PositiveIntegerField(default=0)  
    po3 = models.PositiveIntegerField(default=0)  
    po4 = models.PositiveIntegerField(default=0)  
    po5 = models.PositiveIntegerField(default=0)  
    po6 = models.PositiveIntegerField(default=0)  
    po7 = models.PositiveIntegerField(default=0)  
    po8 = models.PositiveIntegerField(default=0)  
    po9 = models.PositiveIntegerField(default=0)  
    po10 = models.PositiveIntegerField(default=0)  
    po11 = models.PositiveIntegerField(default=0)  
    po12 = models.PositiveIntegerField(default=0)  
    pso1 = models.PositiveIntegerField(default=0)  
    pso2 = models.PositiveIntegerField(default=0)  
    pso3 = models.PositiveIntegerField(default=0)  
    pso4 = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.subject_name}"
    
class CO6(models.Model):
    subject_name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    po1 = models.PositiveIntegerField(default=0)  # Initial value is 0
    po2 = models.PositiveIntegerField(default=0)  
    po3 = models.PositiveIntegerField(default=0)  
    po4 = models.PositiveIntegerField(default=0)  
    po5 = models.PositiveIntegerField(default=0)  
    po6 = models.PositiveIntegerField(default=0)  
    po7 = models.PositiveIntegerField(default=0)  
    po8 = models.PositiveIntegerField(default=0)  
    po9 = models.PositiveIntegerField(default=0)  
    po10 = models.PositiveIntegerField(default=0)  
    po11 = models.PositiveIntegerField(default=0)  
    po12 = models.PositiveIntegerField(default=0)  
    pso1 = models.PositiveIntegerField(default=0)  
    pso2 = models.PositiveIntegerField(default=0)  
    pso3 = models.PositiveIntegerField(default=0)  
    pso4 = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.subject_name}"
    
class CO7(models.Model):
    subject_name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    po1 = models.PositiveIntegerField(default=0)  # Initial value is 0
    po2 = models.PositiveIntegerField(default=0)  
    po3 = models.PositiveIntegerField(default=0)  
    po4 = models.PositiveIntegerField(default=0)  
    po5 = models.PositiveIntegerField(default=0)  
    po6 = models.PositiveIntegerField(default=0)  
    po7 = models.PositiveIntegerField(default=0)  
    po8 = models.PositiveIntegerField(default=0)  
    po9 = models.PositiveIntegerField(default=0)  
    po10 = models.PositiveIntegerField(default=0)  
    po11 = models.PositiveIntegerField(default=0)  
    po12 = models.PositiveIntegerField(default=0)  
    pso1 = models.PositiveIntegerField(default=0)  
    pso2 = models.PositiveIntegerField(default=0)  
    pso3 = models.PositiveIntegerField(default=0)  
    pso4 = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.subject_name}"
    
