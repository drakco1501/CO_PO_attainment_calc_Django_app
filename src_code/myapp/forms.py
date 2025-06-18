from django.forms import ModelForm
from .models import *
from django import forms

class QuestionsForm(ModelForm):
    class Meta:
        model = Questions
        fields = [
            'IA1_1a_que','IA1_1a_co_val','IA1_1b_que','IA1_1b_co_val',
            'IA1_2a_que','IA1_2a_co_val','IA1_2b_que','IA1_2b_co_val',
            'IA2_1a_que','IA2_1a_co_val','IA2_1b_que','IA2_1b_co_val',
            'IA2_2a_que','IA2_2a_co_val','IA2_2b_que','IA2_2b_co_val',
        ]
        widgets = {
            'IA1_1a_co_val': forms.NumberInput(attrs={
                'min': '0',
                'max': '7'
            }),
            'IA1_1b_co_val': forms.NumberInput(attrs={
                'min': '0',
                'max': '7'
            }),
            'IA1_2a_co_val': forms.NumberInput(attrs={
                'min': '0',
                'max': '7'
            }),
            'IA1_2b_co_val': forms.NumberInput(attrs={
                'min': '0',
                'max': '7'
            }),
            'IA2_1a_co_val': forms.NumberInput(attrs={
                'min': '0',
                'max': '7'
            }),
            'IA2_1b_co_val': forms.NumberInput(attrs={
                'min': '0',
                'max': '7'
            }),
            'IA2_2a_co_val': forms.NumberInput(attrs={
                'min': '0',
                'max': '7'
            }),
            'IA2_2b_co_val': forms.NumberInput(attrs={
                'min': '0',
                'max': '7'
            }),
        }
        
class MarksForm(ModelForm):
    class Meta:
        model = Marks
        fields = [
            'IA1_1a', 'IA1_1b', 'IA1_2a', 'IA1_2b', 
            'IA2_1a', 'IA2_1b', 'IA2_2a', 'IA2_2b', 
        ]
        # Method 1: Using widgets in Meta class
        widgets = {
            'IA1_1a': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter marks (0-20)',
                'min': '0',
                'max': '100'
            }),
            'IA1_1b': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter marks (0-20)',
                'min': '0',
                'max': '100'
            }),
            'IA1_2a': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter marks (0-20)',
                'min': '0',
                'max': '100'
            }),
            'IA1_2b': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter marks (0-20)',
                'min': '0',
                'max': '100'
            }),
            'IA2_1a': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter marks (0-20)',
                'min': '0',
                'max': '100'
            }),
            'IA2_1b': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter marks (0-20)',
                'min': '0',
                'max': '100'
            }),
            'IA2_2a': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter marks (0-20)',
                'min': '0',
                'max': '100'
            }),
            'IA2_2b': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter marks (0-20)',
                'min': '0',
                'max': '100'
            }),
        }


class NumberOfCOForm(ModelForm):
    class Meta:
        model = NumberOfCO
        fields = ['num_co_value',]
        widgets = {
            'num_co_value': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter COs required',
                'min': '0',
                'max': '7'
            }),
        }

class CO1Form(ModelForm):
    class Meta:
        model = CO1
        fields = [ 'po1','po2','po3','po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10',  
                    'po11', 'po12', 'pso1', 'pso2', 'pso3', 'pso4']
        widgets = {
            'po1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po5': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '10'
            }),
            'po6': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po7': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po8': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po9': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po10': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po11': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po12': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
        }

class CO2Form(ModelForm):
    class Meta:
        model = CO2
        fields = [ 'po1','po2','po3','po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10',  
                    'po11', 'po12', 'pso1', 'pso2', 'pso3', 'pso4']
        widgets = {
            'po1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po5': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po6': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po7': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po8': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po9': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po10': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po11': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po12': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
        }


class CO3Form(ModelForm):
    class Meta:
        model = CO3
        fields = [ 'po1','po2','po3','po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10',  
                    'po11', 'po12', 'pso1', 'pso2', 'pso3', 'pso4']
        widgets = {
            'po1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po5': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po6': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po7': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po8': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po9': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po10': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po11': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po12': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
        }


class CO4Form(ModelForm):
    class Meta:
        model = CO4
        fields = [ 'po1','po2','po3','po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10',  
                    'po11', 'po12', 'pso1', 'pso2', 'pso3', 'pso4']
        widgets = {
            'po1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po5': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po6': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po7': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po8': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po9': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po10': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po11': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po12': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
        }


class CO5Form(ModelForm):
    class Meta:
        model = CO5
        fields = [ 'po1','po2','po3','po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10',  
                    'po11', 'po12', 'pso1', 'pso2', 'pso3', 'pso4']
        widgets = {
            'po1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po5': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po6': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po7': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po8': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po9': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po10': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po11': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po12': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
        }


class CO6Form(ModelForm):
    class Meta:
        model = CO6
        fields = [ 'po1','po2','po3','po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10',  
                    'po11', 'po12', 'pso1', 'pso2', 'pso3', 'pso4']
        widgets = {
            'po1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po5': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po6': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po7': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po8': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po9': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po10': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po11': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po12': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
        }


class CO7Form(ModelForm):
    class Meta:
        model = CO7
        fields = [ 'po1','po2','po3','po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10',  
                    'po11', 'po12', 'pso1', 'pso2', 'pso3', 'pso4']
        widgets = {
            'po1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po5': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po6': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po7': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po8': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po9': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po10': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po11': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'po12': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso1': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso2': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso3': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
            'pso4': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'max': '3'
            }),
        }