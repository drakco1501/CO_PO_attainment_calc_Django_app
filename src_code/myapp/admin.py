from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name', 'password')
    search_fields = ('subject_name',)


@admin.register(NumberOfCO)
class NumberOfCOAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'num_co_value')  # Display subject_name and num_co_value
    search_fields = ('subject_name',)  # Enable search by subject name
    list_editable = ('num_co_value',)  # Allow inline editing of num_co_value
    list_filter = ('subject_name',)  

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','student_name', 'roll_number')


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'student_name', 'roll_number')


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('subject_name',)


@admin.register(CO1)
class CO1Admin(admin.ModelAdmin):
    list_display = ('subject_name',)

@admin.register(CO2)
class CO2Admin(admin.ModelAdmin):
    list_display = ('subject_name',)

@admin.register(CO3)
class CO3Admin(admin.ModelAdmin):
    list_display = ('subject_name',)

@admin.register(CO4)
class CO4Admin(admin.ModelAdmin):
    list_display = ('subject_name',)

@admin.register(CO5)
class CO5Admin(admin.ModelAdmin):
    list_display = ('subject_name',)

@admin.register(CO6)
class CO6Admin(admin.ModelAdmin):
    list_display = ('subject_name',)

@admin.register(CO7)
class CO7Admin(admin.ModelAdmin):
    list_display = ('subject_name',)
