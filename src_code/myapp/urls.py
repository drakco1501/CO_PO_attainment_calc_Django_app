from django.urls import path
from .views import *

urlpatterns = [
    path('', user_login, name='login'),
    path('login/', user_login, name='user_login'),  # Added for form action
    path('logout/', user_logout, name='user_logout'),
    path('home/', home, name='home'),
    path('questions/', questions, name='questions'),
    path('update_questions/', update_questions, name='update_questions'),
    path('marks/', marks, name='marks'),
    path('marks_update/<str:stu_id>/', marks_update, name='marks_update'),
    path('attainment/', attainment, name='attainment'),
    path('co_val_form/', co_val_form, name='co_val_form'),
    path('clear_co/', clear_co, name='clear_co'),
    path('update_co/<str:co_val>/', update_co, name='update_co'),
    path('calculate/', calculate, name='calculate'),

]