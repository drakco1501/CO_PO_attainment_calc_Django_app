from django.contrib.auth.backends import BaseBackend
from .models import Teacher
from django.contrib.auth.hashers import check_password

class TeacherBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            teacher = Teacher.objects.get(subject_name=username)
            if check_password(password, teacher.password):
                return teacher
        except Teacher.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Teacher.objects.get(pk=user_id)
        except Teacher.DoesNotExist:
            return None