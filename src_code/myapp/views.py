from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.hashers import check_password
from .models import *
from .forms import *



# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Find teacher by subject_name (used as username)
            teacher = Teacher.objects.get(subject_name=username)
            
            # Check if password matches
            if check_password(password, teacher.password):
                # Store teacher info in session
                request.session['teacher_id'] = teacher.id
                request.session['subject_name'] = teacher.subject_name
                request.session['is_teacher_logged_in'] = True
                
                messages.success(request, f'Welcome, {teacher.subject_name}')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        
        except Teacher.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'myapp/login.html')

def user_logout(request):
    # Clear teacher session data
    if 'teacher_id' in request.session:
        del request.session['teacher_id']
    if 'teacher_subject' in request.session:
        del request.session['teacher_subject']
    if 'is_teacher_logged_in' in request.session:
        del request.session['is_teacher_logged_in']
    
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_teacher_logged_in'):
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@user_login_required
def home(request):
    return render(request, 'myapp/home.html')

@user_login_required
def questions(request):
    subject = Questions.objects.get(subject_name = request.session['subject_name'])
    context = {
        'subject' : subject,
    }
    return render(request, 'myapp/questions.html', context)


def update_questions(request):
    try:
        subject = Questions.objects.get(subject_name=request.session['subject_name'])
    except Questions.DoesNotExist:
        # Handle case where subject doesn't exist
        return redirect('home')  # or show an error message
    
    if request.method == 'POST':
        form = QuestionsForm(request.POST, instance=subject)  # Pass instance here
        form.save()
        return redirect('questions') 
        # If form is not valid, it will fall through and render the template with errors
    else:
        form = QuestionsForm(instance=subject)
    
    context = {
        'form': form,
    }
    return render(request, 'myapp/questions_update.html', context)

@user_login_required
def marks(request):
    students = Marks.objects.filter(subject_name=request.session['subject_name'])
    stu_count = Marks.objects.filter(subject_name=request.session['subject_name']).count
    context = {
        'students' : students,
        'stu_count': stu_count,
    }
    return render(request, 'myapp/marks.html', context)

def marks_update(request, stu_id):
    try:
        student = Marks.objects.get(id = stu_id)
    except Marks.DoesNotExist:
        return redirect('home') 
    
    if request.method == 'POST':
        form = MarksForm(request.POST, instance=student)  # Pass instance here
        form.save()
        return redirect('marks') 
        # If form is not valid, it will fall through and render the template with errors
    else:
        form = MarksForm(instance=student)
    

    context = {
        'student': student,
        'form' : form,
    }
    return render(request, 'myapp/marks_update.html',context)

def co_val_form(request):

    try:
        co_num = NumberOfCO.objects.get(subject_name=request.session['subject_name'])
    except NumberOfCO.DoesNotExist:
        return redirect('home') 
    
    if request.method == 'POST' :
        form = NumberOfCOForm(request.POST , instance=co_num)
        form.save()
        return redirect('attainment')
    else:
        form = NumberOfCOForm(instance=co_num)

    context = {
        'form' : form,
        'co_num' : co_num,
    }
    return render(request, 'myapp/co_val_form.html', context)

def clear_co(request):
    co_num = NumberOfCO.objects.get(subject_name=request.session['subject_name'])
    co_num.num_co_value = 0
    co_num.save()
    return redirect('co_val_form')


def attainment(request):
    co_num = NumberOfCO.objects.get(subject_name=request.session['subject_name'])
    if co_num.num_co_value == 0:
        return redirect('co_val_form')
    else:
        count = co_num.num_co_value
        co_objects = {}
        
        # Dynamically fetch CO objects and store them in the context
        for i in range(1, count + 1):
            co_model = globals().get(f'CO{i}')
            if co_model:
                co_objects[f'Co{i}'] = co_model.objects.get(subject_name=request.session['subject_name'])
        
        context = {
            **co_objects,
            'count': count,
        }
    
        
    return render(request, 'myapp/attainment.html', context)

CO_MODELS = {
    1: (CO1, CO1Form),
    2: (CO2, CO2Form),
    3: (CO3, CO3Form),
    4: (CO4, CO4Form),
    5: (CO5, CO5Form),
    6: (CO6, CO6Form),
    7: (CO7, CO7Form),
}

def update_co(request, co_val):
    try:
        co_model, co_form = CO_MODELS.get(int(co_val))
        co = co_model.objects.get(subject_name=request.session['subject_name'])
    except (KeyError, ValueError, co_model.DoesNotExist):
        messages.error(request, 'Invalid CO value or ID not found.')
        return redirect('attainment')

    if request.method == 'POST':
        form = co_form(request.POST, instance=co)
        if form.is_valid():
            form.save()
            return redirect('attainment')
        else:
            messages.error(request, 'Form is invalid.')
    else:
        form = co_form(instance=co)
    
    context = {
        'form': form,
        'val' : co_val,
    }
    return render(request, 'myapp/update_co.html', context)



def calculate(request):
    averages = Marks.objects.filter(subject_name=request.session['subject_name']).aggregate(
        avg_IA1_1a=Avg('IA1_1a'),
        avg_IA1_1b=Avg('IA1_1b'),
        avg_IA1_2a=Avg('IA1_2a'),
        avg_IA1_2b=Avg('IA1_2b'),
        avg_IA2_1a=Avg('IA2_1a'),
        avg_IA2_1b=Avg('IA2_1b'),
        avg_IA2_2a=Avg('IA2_2a'),
        avg_IA2_2b=Avg('IA2_2b'),
    )

    # Access the calculated averages
    avg_IA1_1a = averages['avg_IA1_1a']
    avg_IA1_1b = averages['avg_IA1_1b']
    avg_IA1_2a = averages['avg_IA1_2a']
    avg_IA1_2b = averages['avg_IA1_2b']
    avg_IA2_1a = averages['avg_IA2_1a']
    avg_IA2_1b = averages['avg_IA2_1b']
    avg_IA2_2a = averages['avg_IA2_2a']
    avg_IA2_2b = averages['avg_IA2_2b']

    if avg_IA1_1a >= 50 :
        IA1_1a_co_val = 3
    elif avg_IA1_1a < 50 and avg_IA1_1a > 30 :
        IA1_1a_co_val = 2
    elif avg_IA1_1a < 30 and avg_IA1_1a >= 1 :
        IA1_1a_co_val = 1
    else:
        IA1_1a_co_val = 0

    if avg_IA1_1b >= 50 :
        IA1_1b_co_val = 3
    elif avg_IA1_1b < 50 and avg_IA1_1b > 30 :
        IA1_1b_co_val = 2
    elif avg_IA1_1b < 30 and avg_IA1_1b >= 1 :
        IA1_1b_co_val = 1
    else:
        IA1_1b_co_val = 0
    
    if avg_IA1_2a >= 50 :
        IA1_2a_co_val = 3
    elif avg_IA1_2a < 50 and avg_IA1_2a > 30 :
        IA1_2a_co_val = 2
    elif avg_IA1_2a < 30 and avg_IA1_2a >= 1 :
        IA1_2a_co_val = 1
    else:
        IA1_2a_co_val = 0

    if avg_IA1_2b >= 50 :
        IA1_2b_co_val = 3
    elif avg_IA1_2b < 50 and avg_IA1_2b > 30 :
        IA1_2b_co_val = 2
    elif avg_IA1_2b < 30 and avg_IA1_2b >= 1 :
        IA1_2b_co_val = 1
    else:
        IA1_2b_co_val = 0



    if avg_IA2_1a >= 50 :
        IA2_1a_co_val = 3
    elif avg_IA2_1a < 50 and avg_IA1_1a > 30 :
        IA2_1a_co_val = 2
    elif avg_IA2_1a < 30 and avg_IA1_1a >= 1 :
        IA2_1a_co_val = 1
    else:
        IA2_1a_co_val = 0

    if avg_IA2_1b >= 50 :
        IA2_1b_co_val = 3
    elif avg_IA2_1b < 50 and avg_IA1_1b > 30 :
        IA2_1b_co_val = 2
    elif avg_IA2_1b < 30 and avg_IA1_1b >= 1 :
        IA2_1b_co_val = 1
    else:
        IA2_1b_co_val = 0
    
    if avg_IA2_2a >= 50 :
        IA2_2a_co_val = 3
    elif avg_IA2_2a < 50 and avg_IA1_2a > 30 :
        IA2_2a_co_val = 2
    elif avg_IA2_2a < 30 and avg_IA1_2a >= 1 :
        IA2_2a_co_val = 1
    else:
        IA2_2a_co_val = 0

    if avg_IA2_2b >= 50 :
        IA2_2b_co_val = 3
    elif avg_IA2_2b < 50 and avg_IA1_2b > 30 :
        IA2_2b_co_val = 2
    elif avg_IA2_2b < 30 and avg_IA1_2b >= 1 :
        IA2_2b_co_val = 1
    else:
        IA2_2b_co_val = 0

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0

    co1_attainment = 0 
    co2_attainment = 0 
    co3_attainment = 0 
    co4_attainment = 0 
    co5_attainment = 0 
    co6_attainment = 0 
    co7_attainment = 0 

    co_map = Questions.objects.get(subject_name = request.session['subject_name'])

    if co_map.IA1_1a_co_val == 1:
        co1_attainment += IA1_1a_co_val
        count1 += 1
    elif co_map.IA1_1a_co_val == 2:
        co2_attainment += IA1_1a_co_val
        count2 += 1
    elif co_map.IA1_1a_co_val == 3:
        co3_attainment += IA1_1a_co_val
        count3 += 1
    elif co_map.IA1_1a_co_val == 4:
        co4_attainment += IA1_1a_co_val
        count4 += 1
    elif co_map.IA1_1a_co_val == 5:
        co5_attainment += IA1_1a_co_val
        count5 += 1
    elif co_map.IA1_1a_co_val == 6:
        co6_attainment += IA1_1a_co_val
        count6 += 1
    elif co_map.IA1_1a_co_val == 7:
        co7_attainment += IA1_1a_co_val
        count7 += 1



    if co_map.IA1_1b_co_val == 1:
        co1_attainment += IA1_1b_co_val
        count1 += 1
    elif co_map.IA1_1b_co_val == 2:
        co2_attainment += IA1_1b_co_val
        count2 += 1
    elif co_map.IA1_1b_co_val == 3:
        co3_attainment += IA1_1b_co_val
        count3 += 1
    elif co_map.IA1_1b_co_val == 4:
        co4_attainment += IA1_1b_co_val
        count4 += 1
    elif co_map.IA1_1b_co_val == 5:
        co5_attainment += IA1_1b_co_val
        count5 += 1
    elif co_map.IA1_1b_co_val == 6:
        co6_attainment += IA1_1b_co_val
        count6 += 1
    elif co_map.IA1_1b_co_val == 7:
        co7_attainment += IA1_1b_co_val
        count7 += 1

    if co_map.IA1_2a_co_val == 1:
        co1_attainment += IA1_2a_co_val
        count1 += 1
    elif co_map.IA1_2a_co_val == 2:
        co2_attainment += IA1_2a_co_val
        count2 += 1
    elif co_map.IA1_2a_co_val == 3:
        co3_attainment += IA1_2a_co_val
        count3 += 1
    elif co_map.IA1_2a_co_val == 4:
        co4_attainment += IA1_2a_co_val
        count4 += 1
    elif co_map.IA1_2a_co_val == 5:
        co5_attainment += IA1_1a_co_val
        count5 += 1
    elif co_map.IA1_2a_co_val == 6:
        co6_attainment += IA1_2a_co_val
        count6 += 1
    elif co_map.IA1_2a_co_val == 7:
        co7_attainment += IA1_2a_co_val
        count7 += 1



    if co_map.IA1_2b_co_val == 1:
        co1_attainment += IA1_2b_co_val
        count1 += 1
    elif co_map.IA1_2b_co_val == 2:
        co2_attainment += IA1_2b_co_val
        count2 += 1
    elif co_map.IA1_2b_co_val == 3:
        co3_attainment += IA1_2b_co_val
        count3 += 1
    elif co_map.IA1_2b_co_val == 4:
        co4_attainment += IA1_2b_co_val
        count4 += 1
    elif co_map.IA1_2b_co_val == 5:
        co5_attainment += IA1_1b_co_val
        count5 += 1
    elif co_map.IA1_2b_co_val == 6:
        co6_attainment += IA1_2b_co_val
        count6 += 1
    elif co_map.IA1_2b_co_val == 7:
        co7_attainment += IA1_2b_co_val
        count7 += 1

    if co_map.IA2_1a_co_val == 1:
        co1_attainment += IA2_1a_co_val
        count1 += 1
    elif co_map.IA2_1a_co_val == 2:
        co2_attainment += IA2_1a_co_val
        count2 += 1
    elif co_map.IA2_1a_co_val == 3:
        co3_attainment += IA2_1a_co_val
        count3 += 1
    elif co_map.IA1_1a_co_val == 4:
        co4_attainment += IA1_1a_co_val
        count4 += 1
    elif co_map.IA2_1a_co_val == 5:
        co5_attainment += IA2_1a_co_val
        count5 += 1
    elif co_map.IA2_1a_co_val == 6:
        co6_attainment += IA2_1a_co_val
        count6 += 1
    elif co_map.IA2_1a_co_val == 7:
        co7_attainment += IA2_1a_co_val
        count7 += 1



    if co_map.IA2_1b_co_val == 1:
        co1_attainment += IA2_1b_co_val
        count1 += 1
    elif co_map.IA2_1b_co_val == 2:
        co2_attainment += IA2_1b_co_val
        count2 += 1
    elif co_map.IA2_1b_co_val == 3:
        co3_attainment += IA2_1b_co_val
        count3 += 1
    elif co_map.IA1_1b_co_val == 4:
        co4_attainment += IA1_1b_co_val
        count4 += 1
    elif co_map.IA2_1b_co_val == 5:
        co5_attainment += IA2_1b_co_val
        count5 += 1
    elif co_map.IA2_1b_co_val == 6:
        co6_attainment += IA2_1b_co_val
        count6 += 1
    elif co_map.IA2_1b_co_val == 7:
        co7_attainment += IA2_1b_co_val
        count7 += 1

    if co_map.IA2_2a_co_val == 1:
        co1_attainment += IA2_2a_co_val
        count1 += 1
    elif co_map.IA2_2a_co_val == 2:
        co2_attainment += IA2_2a_co_val
        count2 += 1
    elif co_map.IA2_2a_co_val == 3:
        co3_attainment += IA2_2a_co_val
        count3 += 1
    elif co_map.IA1_2a_co_val == 4:
        co4_attainment += IA1_2a_co_val
        count4 += 1
    elif co_map.IA2_2a_co_val == 5:
        co5_attainment += IA2_1a_co_val
        count5 += 1
    elif co_map.IA2_2a_co_val == 6:
        co6_attainment += IA2_2a_co_val
        count6 += 1
    elif co_map.IA2_2a_co_val == 7:
        co7_attainment += IA2_2a_co_val
        count7 += 1



    if co_map.IA2_2b_co_val == 1:
        co1_attainment += IA2_2b_co_val
        count1 += 1
    elif co_map.IA2_2b_co_val == 2:
        co2_attainment += IA2_2b_co_val
        count2 += 1
    elif co_map.IA2_2b_co_val == 3:
        co3_attainment += IA2_2b_co_val
        count3 += 1
    elif co_map.IA1_2b_co_val == 4:
        co4_attainment += IA1_2b_co_val
        count4 += 1
    elif co_map.IA2_2b_co_val == 5:
        co5_attainment += IA2_1b_co_val
        count5 += 1
    elif co_map.IA2_2b_co_val == 6:
        co6_attainment += IA2_2b_co_val
        count6 += 1
    elif co_map.IA2_2b_co_val == 7:
        co7_attainment += IA2_2b_co_val
        count7 += 1

    co1_attainment = co1_attainment / count1 if count1 != 0 else 0
    co2_attainment = co2_attainment / count2 if count2 != 0 else 0
    co3_attainment = co3_attainment / count3 if count3 != 0 else 0
    co4_attainment = co4_attainment / count4 if count4 != 0 else 0
    co5_attainment = co5_attainment / count5 if count5 != 0 else 0
    co6_attainment = co6_attainment / count6 if count6 != 0 else 0
    co7_attainment = co7_attainment / count7 if count7 != 0 else 0


    num_of_co = NumberOfCO.objects.get(subject_name=request.session['subject_name'])
    num_co = num_of_co.num_co_value

    if num_co == 1:
        co1 = CO1.objects.get(subject_name=request.session['subject_name'])

        def safe_division(numerator, denominator):
            return numerator / denominator if denominator != 0 else 0

        po1 = safe_division(co1.po1 * co1_attainment, co1.po1)
        po2 = safe_division(co1.po2 * co1_attainment, co1.po2)
        po3 = safe_division(co1.po3 * co1_attainment, co1.po3)
        po4 = safe_division(co1.po4 * co1_attainment, co1.po4)
        po5 = safe_division(co1.po5 * co1_attainment, co1.po5)
        po6 = safe_division(co1.po6 * co1_attainment, co1.po6)
        po7 = safe_division(co1.po7 * co1_attainment, co1.po7)
        po8 = safe_division(co1.po8 * co1_attainment, co1.po8)
        po9 = safe_division(co1.po9 * co1_attainment, co1.po9)
        po10 = safe_division(co1.po10 * co1_attainment, co1.po10)
        po11 = safe_division(co1.po11 * co1_attainment, co1.po11)
        po12 = safe_division(co1.po12 * co1_attainment, co1.po12)
        pso1 = safe_division(co1.pso1 * co1_attainment, co1.pso1)
        pso2 = safe_division(co1.pso2 * co1_attainment, co1.pso2)
        pso3 = safe_division(co1.pso3 * co1_attainment, co1.pso3)
        pso4 = safe_division(co1.pso4 * co1_attainment, co1.pso4)

    
    if num_co == 2:
        co1 = CO1.objects.get(subject_name=request.session['subject_name'])
        co2 = CO2.objects.get(subject_name=request.session['subject_name'])

        def safe_division(numerator, denominator):
            return numerator / denominator if denominator != 0 else 0

        po1 = safe_division((co1.po1 * co1_attainment) + (co2.po1 * co2_attainment), co1.po1 + co2.po1)
        po2 = safe_division((co1.po2 * co1_attainment) + (co2.po2 * co2_attainment), co1.po2 + co2.po2)
        po3 = safe_division((co1.po3 * co1_attainment) + (co2.po3 * co2_attainment), co1.po3 + co2.po3)
        po4 = safe_division((co1.po4 * co1_attainment) + (co2.po4 * co2_attainment), co1.po4 + co2.po4)
        po5 = safe_division((co1.po5 * co1_attainment) + (co2.po5 * co2_attainment), co1.po5 + co2.po5)
        po6 = safe_division((co1.po6 * co1_attainment) + (co2.po6 * co2_attainment), co1.po6 + co2.po6)
        po7 = safe_division((co1.po7 * co1_attainment) + (co2.po7 * co2_attainment), co1.po7 + co2.po7)
        po8 = safe_division((co1.po8 * co1_attainment) + (co2.po8 * co2_attainment), co1.po8 + co2.po8)
        po9 = safe_division((co1.po9 * co1_attainment) + (co2.po9 * co2_attainment), co1.po9 + co2.po9)
        po10 = safe_division((co1.po10 * co1_attainment) + (co2.po10 * co2_attainment), co1.po10 + co2.po10)
        po11 = safe_division((co1.po11 * co1_attainment) + (co2.po11 * co2_attainment), co1.po11 + co2.po11)
        po12 = safe_division((co1.po12 * co1_attainment) + (co2.po12 * co2_attainment), co1.po12 + co2.po12)
        pso1 = safe_division((co1.pso1 * co1_attainment) + (co2.pso1 * co2_attainment), co1.pso1 + co2.pso1)
        pso2 = safe_division((co1.pso2 * co1_attainment) + (co2.pso2 * co2_attainment), co1.pso2 + co2.pso2)
        pso3 = safe_division((co1.pso3 * co1_attainment) + (co2.pso3 * co2_attainment), co1.pso3 + co2.pso3)
        pso4 = safe_division((co1.pso4 * co1_attainment) + (co2.pso4 * co2_attainment), co1.pso4 + co2.pso4)


    if num_co == 3:
        co1 = CO1.objects.get(subject_name=request.session['subject_name'])
        co2 = CO2.objects.get(subject_name=request.session['subject_name'])
        co3 = CO3.objects.get(subject_name=request.session['subject_name'])

        def safe_division(numerator, denominator):
            return numerator / denominator if denominator != 0 else 0

        po1 = safe_division((co1.po1 * co1_attainment) + (co2.po1 * co2_attainment) + (co3.po1 * co3_attainment), co1.po1 + co2.po1 + co3.po1)
        po2 = safe_division((co1.po2 * co1_attainment) + (co2.po2 * co2_attainment) + (co3.po2 * co3_attainment), co1.po2 + co2.po2 + co3.po2)
        po3 = safe_division((co1.po3 * co1_attainment) + (co2.po3 * co2_attainment) + (co3.po3 * co3_attainment), co1.po3 + co2.po3 + co3.po3)
        po4 = safe_division((co1.po4 * co1_attainment) + (co2.po4 * co2_attainment) + (co3.po4 * co3_attainment), co1.po4 + co2.po4 + co3.po4)
        po5 = safe_division((co1.po5 * co1_attainment) + (co2.po5 * co2_attainment) + (co3.po5 * co3_attainment), co1.po5 + co2.po5 + co3.po5)
        po6 = safe_division((co1.po6 * co1_attainment) + (co2.po6 * co2_attainment) + (co3.po6 * co3_attainment), co1.po6 + co2.po6 + co3.po6)
        po7 = safe_division((co1.po7 * co1_attainment) + (co2.po7 * co2_attainment) + (co3.po7 * co3_attainment), co1.po7 + co2.po7 + co3.po7)
        po8 = safe_division((co1.po8 * co1_attainment) + (co2.po8 * co2_attainment) + (co3.po8 * co3_attainment), co1.po8 + co2.po8 + co3.po8)
        po9 = safe_division((co1.po9 * co1_attainment) + (co2.po9 * co2_attainment) + (co3.po9 * co3_attainment), co1.po9 + co2.po9 + co3.po9)
        po10 = safe_division((co1.po10 * co1_attainment) + (co2.po10 * co2_attainment) + (co3.po10 * co3_attainment), co1.po10 + co2.po10 + co3.po10)
        po11 = safe_division((co1.po11 * co1_attainment) + (co2.po11 * co2_attainment) + (co3.po11 * co3_attainment), co1.po11 + co2.po11 + co3.po11)
        po12 = safe_division((co1.po12 * co1_attainment) + (co2.po12 * co2_attainment) + (co3.po12 * co3_attainment), co1.po12 + co2.po12 + co3.po12)
        pso1 = safe_division((co1.pso1 * co1_attainment) + (co2.pso1 * co2_attainment) + (co3.pso1 * co3_attainment), co1.pso1 + co2.pso1 + co3.pso1)
        pso2 = safe_division((co1.pso2 * co1_attainment) + (co2.pso2 * co2_attainment) + (co3.pso2 * co3_attainment), co1.pso2 + co2.pso2 + co3.pso2)
        pso3 = safe_division((co1.pso3 * co1_attainment) + (co2.pso3 * co2_attainment) + (co3.pso3 * co3_attainment), co1.pso3 + co2.pso3 + co3.pso3)
        pso4 = safe_division((co1.pso4 * co1_attainment) + (co2.pso4 * co2_attainment) + (co3.pso4 * co3_attainment), co1.pso4 + co2.pso4 + co3.pso4)

    if num_co == 4:
        co1 = CO1.objects.get(subject_name=request.session['subject_name'])
        co2 = CO2.objects.get(subject_name=request.session['subject_name'])
        co3 = CO3.objects.get(subject_name=request.session['subject_name'])
        co4 = CO4.objects.get(subject_name=request.session['subject_name'])

        def safe_division(numerator, denominator):
            return numerator / denominator if denominator != 0 else 0

        po1 = safe_division((co1.po1 * co1_attainment) + (co2.po1 * co2_attainment) + (co3.po1 * co3_attainment) + (co4.po1 * co4_attainment), co1.po1 + co2.po1 + co3.po1 + co4.po1)
        po2 = safe_division((co1.po2 * co1_attainment) + (co2.po2 * co2_attainment) + (co3.po2 * co3_attainment) + (co4.po2 * co4_attainment), co1.po2 + co2.po2 + co3.po2 + co4.po2)
        po3 = safe_division((co1.po3 * co1_attainment) + (co2.po3 * co2_attainment) + (co3.po3 * co3_attainment) + (co4.po3 * co4_attainment), co1.po3 + co2.po3 + co3.po3 + co4.po3)
        po4 = safe_division((co1.po4 * co1_attainment) + (co2.po4 * co2_attainment) + (co3.po4 * co3_attainment) + (co4.po4 * co4_attainment), co1.po4 + co2.po4 + co3.po4 + co4.po4)
        po5 = safe_division((co1.po5 * co1_attainment) + (co2.po5 * co2_attainment) + (co3.po5 * co3_attainment) + (co4.po5 * co4_attainment), co1.po5 + co2.po5 + co3.po5 + co4.po5)
        po6 = safe_division((co1.po6 * co1_attainment) + (co2.po6 * co2_attainment) + (co3.po6 * co3_attainment) + (co4.po6 * co4_attainment), co1.po6 + co2.po6 + co3.po6 + co4.po6)
        po7 = safe_division((co1.po7 * co1_attainment) + (co2.po7 * co2_attainment) + (co3.po7 * co3_attainment) + (co4.po7 * co4_attainment), co1.po7 + co2.po7 + co3.po7 + co4.po7)
        po8 = safe_division((co1.po8 * co1_attainment) + (co2.po8 * co2_attainment) + (co3.po8 * co3_attainment) + (co4.po8 * co4_attainment), co1.po8 + co2.po8 + co3.po8 + co4.po8)
        po9 = safe_division((co1.po9 * co1_attainment) + (co2.po9 * co2_attainment) + (co3.po9 * co3_attainment) + (co4.po9 * co4_attainment), co1.po9 + co2.po9 + co3.po9 + co4.po9)
        po10 = safe_division((co1.po10 * co1_attainment) + (co2.po10 * co2_attainment) + (co3.po10 * co3_attainment) + (co4.po10 * co4_attainment), co1.po10 + co2.po10 + co3.po10 + co4.po10)
        po11 = safe_division((co1.po11 * co1_attainment) + (co2.po11 * co2_attainment) + (co3.po11 * co3_attainment) + (co4.po11 * co4_attainment), co1.po11 + co2.po11 + co3.po11 + co4.po11)
        po12 = safe_division((co1.po12 * co1_attainment) + (co2.po12 * co2_attainment) + (co3.po12 * co3_attainment) + (co4.po12 * co4_attainment), co1.po12 + co2.po12 + co3.po12 + co4.po12)
        pso1 = safe_division((co1.pso1 * co1_attainment) + (co2.pso1 * co2_attainment) + (co3.pso1 * co3_attainment) + (co4.pso1 * co4_attainment), co1.pso1 + co2.pso1 + co3.pso1 + co4.pso1)
        pso2 = safe_division((co1.pso2 * co1_attainment) + (co2.pso2 * co2_attainment) + (co3.pso2 * co3_attainment) + (co4.pso2 * co4_attainment), co1.pso2 + co2.pso2 + co3.pso2 + co4.pso2)
        pso3 = safe_division((co1.pso3 * co1_attainment) + (co2.pso3 * co2_attainment) + (co3.pso3 * co3_attainment) + (co4.pso3 * co4_attainment), co1.pso3 + co2.pso3 + co3.pso3 + co4.pso3)
        pso4 = safe_division((co1.pso4 * co1_attainment) + (co2.pso4 * co2_attainment) + (co3.pso4 * co3_attainment) + (co4.pso4 * co4_attainment), co1.pso4 + co2.pso4 + co3.pso4 + co4.pso4)

    if num_co == 5:
        co1 = CO1.objects.get(subject_name=request.session['subject_name'])
        co2 = CO2.objects.get(subject_name=request.session['subject_name'])
        co3 = CO3.objects.get(subject_name=request.session['subject_name'])
        co4 = CO4.objects.get(subject_name=request.session['subject_name'])
        co5 = CO5.objects.get(subject_name=request.session['subject_name'])

        def safe_division(numerator, denominator):
            return numerator / denominator if denominator != 0 else 0

        po1 = safe_division((co1.po1 * co1_attainment) + (co2.po1 * co2_attainment) + (co3.po1 * co3_attainment) + (co4.po1 * co4_attainment) + (co5.po1 * co5_attainment), co1.po1 + co2.po1 + co3.po1 + co4.po1 + co5.po1)
        po2 = safe_division((co1.po2 * co1_attainment) + (co2.po2 * co2_attainment) + (co3.po2 * co3_attainment) + (co4.po2 * co4_attainment) + (co5.po2 * co5_attainment), co1.po2 + co2.po2 + co3.po2 + co4.po2 + co5.po2)
        po3 = safe_division((co1.po3 * co1_attainment) + (co2.po3 * co2_attainment) + (co3.po3 * co3_attainment) + (co4.po3 * co4_attainment) + (co5.po3 * co5_attainment), co1.po3 + co2.po3 + co3.po3 + co4.po3 + co5.po3)
        po4 = safe_division((co1.po4 * co1_attainment) + (co2.po4 * co2_attainment) + (co3.po4 * co3_attainment) + (co4.po4 * co4_attainment) + (co5.po4 * co5_attainment), co1.po4 + co2.po4 + co3.po4 + co4.po4 + co5.po4)
        po5 = safe_division((co1.po5 * co1_attainment) + (co2.po5 * co2_attainment) + (co3.po5 * co3_attainment) + (co4.po5 * co4_attainment) + (co5.po5 * co5_attainment), co1.po5 + co2.po5 + co3.po5 + co4.po5 + co5.po5)
        po6 = safe_division((co1.po6 * co1_attainment) + (co2.po6 * co2_attainment) + (co3.po6 * co3_attainment) + (co4.po6 * co4_attainment) + (co5.po6 * co5_attainment), co1.po6 + co2.po6 + co3.po6 + co4.po6 + co5.po6)
        po7 = safe_division((co1.po7 * co1_attainment) + (co2.po7 * co2_attainment) + (co3.po7 * co3_attainment) + (co4.po7 * co4_attainment) + (co5.po7 * co5_attainment), co1.po7 + co2.po7 + co3.po7 + co4.po7 + co5.po7)
        po8 = safe_division((co1.po8 * co1_attainment) + (co2.po8 * co2_attainment) + (co3.po8 * co3_attainment) + (co4.po8 * co4_attainment) + (co5.po8 * co5_attainment), co1.po8 + co2.po8 + co3.po8 + co4.po8 + co5.po8)
        po9 = safe_division((co1.po9 * co1_attainment) + (co2.po9 * co2_attainment) + (co3.po9 * co3_attainment) + (co4.po9 * co4_attainment) + (co5.po9 * co5_attainment), co1.po9 + co2.po9 + co3.po9 + co4.po9 + co5.po9)
        po10 = safe_division((co1.po10 * co1_attainment) + (co2.po10 * co2_attainment) + (co3.po10 * co3_attainment) + (co4.po10 * co4_attainment) + (co5.po10 * co5_attainment), co1.po10 + co2.po10 + co3.po10 + co4.po10 + co5.po10)
        po11 = safe_division((co1.po11 * co1_attainment) + (co2.po11 * co2_attainment) + (co3.po11 * co3_attainment) + (co4.po11 * co4_attainment) + (co5.po11 * co5_attainment), co1.po11 + co2.po11 + co3.po11 + co4.po11 + co5.po11)
        po12 = safe_division((co1.po12 * co1_attainment) + (co2.po12 * co2_attainment) + (co3.po12 * co3_attainment) + (co4.po12 * co4_attainment) + (co5.po12 * co5_attainment), co1.po12 + co2.po12 + co3.po12 + co4.po12 + co5.po12)
        pso1 = safe_division((co1.pso1 * co1_attainment) + (co2.pso1 * co2_attainment) + (co3.pso1 * co3_attainment) + (co4.pso1 * co4_attainment) + (co5.pso1 * co5_attainment), co1.pso1 + co2.pso1 + co3.pso1 + co4.pso1 + co5.pso1)
        pso2 = safe_division((co1.pso2 * co1_attainment) + (co2.pso2 * co2_attainment) + (co3.pso2 * co3_attainment) + (co4.pso2 * co4_attainment) + (co5.pso2 * co5_attainment), co1.pso2 + co2.pso2 + co3.pso2 + co4.pso2 + co5.pso2)
        pso3 = safe_division((co1.pso3 * co1_attainment) + (co2.pso3 * co2_attainment) + (co3.pso3 * co3_attainment) + (co4.pso3 * co4_attainment) + (co5.pso3 * co5_attainment), co1.pso3 + co2.pso3 + co3.pso3 + co4.pso3 + co5.pso3)
        pso4 = safe_division((co1.pso4 * co1_attainment) + (co2.pso4 * co2_attainment) + (co3.pso4 * co3_attainment) + (co4.pso4 * co4_attainment) + (co5.pso4 * co5_attainment), co1.pso4 + co2.pso4 + co3.pso4 + co4.pso4 + co5.pso4)

    if num_co == 6:
        co1 = CO1.objects.get(subject_name=request.session['subject_name'])
        co2 = CO2.objects.get(subject_name=request.session['subject_name'])
        co3 = CO3.objects.get(subject_name=request.session['subject_name'])
        co4 = CO4.objects.get(subject_name=request.session['subject_name'])
        co5 = CO5.objects.get(subject_name=request.session['subject_name'])
        co6 = CO6.objects.get(subject_name=request.session['subject_name'])

        def safe_division(numerator, denominator):
            return numerator / denominator if denominator != 0 else 0

        po1 = safe_division(
            (co1.po1 * co1_attainment) + (co2.po1 * co2_attainment) + (co3.po1 * co3_attainment) +
            (co4.po1 * co4_attainment) + (co5.po1 * co5_attainment) + (co6.po1 * co6_attainment),
            co1.po1 + co2.po1 + co3.po1 + co4.po1 + co5.po1 + co6.po1
        )
        po2 = safe_division(
            (co1.po2 * co1_attainment) + (co2.po2 * co2_attainment) + (co3.po2 * co3_attainment) +
            (co4.po2 * co4_attainment) + (co5.po2 * co5_attainment) + (co6.po2 * co6_attainment),
            co1.po2 + co2.po2 + co3.po2 + co4.po2 + co5.po2 + co6.po2
        )
        po3 = safe_division(
            (co1.po3 * co1_attainment) + (co2.po3 * co2_attainment) + (co3.po3 * co3_attainment) +
            (co4.po3 * co4_attainment) + (co5.po3 * co5_attainment) + (co6.po3 * co6_attainment),
            co1.po3 + co2.po3 + co3.po3 + co4.po3 + co5.po3 + co6.po3
        )
        po4 = safe_division(
            (co1.po4 * co1_attainment) + (co2.po4 * co2_attainment) + (co3.po4 * co3_attainment) +
            (co4.po4 * co4_attainment) + (co5.po4 * co5_attainment) + (co6.po4 * co6_attainment),
            co1.po4 + co2.po4 + co3.po4 + co4.po4 + co5.po4 + co6.po4
        )
        po5 = safe_division(
            (co1.po5 * co1_attainment) + (co2.po5 * co2_attainment) + (co3.po5 * co3_attainment) +
            (co4.po5 * co4_attainment) + (co5.po5 * co5_attainment) + (co6.po5 * co6_attainment),
            co1.po5 + co2.po5 + co3.po5 + co4.po5 + co5.po5 + co6.po5
        )
        po6 = safe_division(
            (co1.po6 * co1_attainment) + (co2.po6 * co2_attainment) + (co3.po6 * co3_attainment) +
            (co4.po6 * co4_attainment) + (co5.po6 * co5_attainment) + (co6.po6 * co6_attainment),
            co1.po6 + co2.po6 + co3.po6 + co4.po6 + co5.po6 + co6.po6
        )
        po7 = safe_division(
            (co1.po7 * co1_attainment) + (co2.po7 * co2_attainment) + (co3.po7 * co3_attainment) +
            (co4.po7 * co4_attainment) + (co5.po7 * co5_attainment) + (co6.po7 * co6_attainment),
            co1.po7 + co2.po7 + co3.po7 + co4.po7 + co5.po7 + co6.po7
        )
        po8 = safe_division(
            (co1.po8 * co1_attainment) + (co2.po8 * co2_attainment) + (co3.po8 * co3_attainment) +
            (co4.po8 * co4_attainment) + (co5.po8 * co5_attainment) + (co6.po8 * co6_attainment),
            co1.po8 + co2.po8 + co3.po8 + co4.po8 + co5.po8 + co6.po8
        )
        po9 = safe_division(
            (co1.po9 * co1_attainment) + (co2.po9 * co2_attainment) + (co3.po9 * co3_attainment) +
            (co4.po9 * co4_attainment) + (co5.po9 * co5_attainment) + (co6.po9 * co6_attainment),
            co1.po9 + co2.po9 + co3.po9 + co4.po9 + co5.po9 + co6.po9
        )
        po10 = safe_division(
            (co1.po10 * co1_attainment) + (co2.po10 * co2_attainment) + (co3.po10 * co3_attainment) +
            (co4.po10 * co4_attainment) + (co5.po10 * co5_attainment) + (co6.po10 * co6_attainment),
            co1.po10 + co2.po10 + co3.po10 + co4.po10 + co5.po10 + co6.po10
        )
        po11 = safe_division(
            (co1.po11 * co1_attainment) + (co2.po11 * co2_attainment) + (co3.po11 * co3_attainment) +
            (co4.po11 * co4_attainment) + (co5.po11 * co5_attainment) + (co6.po11 * co6_attainment),
            co1.po11 + co2.po11 + co3.po11 + co4.po11 + co5.po11 + co6.po11
        )
        po12 = safe_division(
            (co1.po12 * co1_attainment) + (co2.po12 * co2_attainment) + (co3.po12 * co3_attainment) +
            (co4.po12 * co4_attainment) + (co5.po12 * co5_attainment) + (co6.po12 * co6_attainment),
            co1.po12 + co2.po12 + co3.po12 + co4.po12 + co5.po12 + co6.po12
        )
        pso1 = safe_division(
            (co1.pso1 * co1_attainment) + (co2.pso1 * co2_attainment) + (co3.pso1 * co3_attainment) +
            (co4.pso1 * co4_attainment) + (co5.pso1 * co5_attainment) + (co6.pso1 * co6_attainment),
            co1.pso1 + co2.pso1 + co3.pso1 + co4.pso1 + co5.pso1 + co6.pso1
        )
        pso2 = safe_division(
            (co1.pso2 * co1_attainment) + (co2.pso2 * co2_attainment) + (co3.pso2 * co3_attainment) +
            (co4.pso2 * co4_attainment) + (co5.pso2 * co5_attainment) + (co6.pso2 * co6_attainment),
            co1.pso2 + co2.pso2 + co3.pso2 + co4.pso2 + co5.pso2 + co6.pso2
        )
        pso3 = safe_division(
            (co1.pso3 * co1_attainment) + (co2.pso3 * co2_attainment) + (co3.pso3 * co3_attainment) +
            (co4.pso3 * co4_attainment) + (co5.pso3 * co5_attainment) + (co6.pso3 * co6_attainment),
            co1.pso3 + co2.pso3 + co3.pso3 + co4.pso3 + co5.pso3 + co6.pso3
        )
        pso4 = safe_division(
            (co1.pso4 * co1_attainment) + (co2.pso4 * co2_attainment) + (co3.pso4 * co3_attainment) +
            (co4.pso4 * co4_attainment) + (co5.pso4 * co5_attainment) + (co6.pso4 * co6_attainment),
            co1.pso4 + co2.pso4 + co3.pso4 + co4.pso4 + co5.pso4 + co6.pso4
        )


    if num_co == 7:
        co1 = CO1.objects.get(subject_name=request.session['subject_name'])
        co2 = CO2.objects.get(subject_name=request.session['subject_name'])
        co3 = CO3.objects.get(subject_name=request.session['subject_name'])
        co4 = CO4.objects.get(subject_name=request.session['subject_name'])
        co5 = CO5.objects.get(subject_name=request.session['subject_name'])
        co6 = CO6.objects.get(subject_name=request.session['subject_name'])
        co7 = CO7.objects.get(subject_name=request.session['subject_name'])

        def safe_division(numerator, denominator):
            return numerator / denominator if denominator != 0 else 0

        po1 = safe_division(
            (co1.po1 * co1_attainment) + (co2.po1 * co2_attainment) + (co3.po1 * co3_attainment) +
            (co4.po1 * co4_attainment) + (co5.po1 * co5_attainment) + (co6.po1 * co6_attainment) +
            (co7.po1 * co7_attainment),
            co1.po1 + co2.po1 + co3.po1 + co4.po1 + co5.po1 + co6.po1 + co7.po1
        )
        po2 = safe_division(
            (co1.po2 * co1_attainment) + (co2.po2 * co2_attainment) + (co3.po2 * co3_attainment) +
            (co4.po2 * co4_attainment) + (co5.po2 * co5_attainment) + (co6.po2 * co6_attainment) +
            (co7.po2 * co7_attainment),
            co1.po2 + co2.po2 + co3.po2 + co4.po2 + co5.po2 + co6.po2 + co7.po2
        )
        po3 = safe_division(
            (co1.po3 * co1_attainment) + (co2.po3 * co2_attainment) + (co3.po3 * co3_attainment) +
            (co4.po3 * co4_attainment) + (co5.po3 * co5_attainment) + (co6.po3 * co6_attainment) +
            (co7.po3 * co7_attainment),
            co1.po3 + co2.po3 + co3.po3 + co4.po3 + co5.po3 + co6.po3 + co7.po3
        )
        po4 = safe_division(
            (co1.po4 * co1_attainment) + (co2.po4 * co2_attainment) + (co3.po4 * co3_attainment) +
            (co4.po4 * co4_attainment) + (co5.po4 * co5_attainment) + (co6.po4 * co6_attainment) +
            (co7.po4 * co7_attainment),
            co1.po4 + co2.po4 + co3.po4 + co4.po4 + co5.po4 + co6.po4 + co7.po4
        )
        po5 = safe_division(
            (co1.po5 * co1_attainment) + (co2.po5 * co2_attainment) + (co3.po5 * co3_attainment) +
            (co4.po5 * co4_attainment) + (co5.po5 * co5_attainment) + (co6.po5 * co6_attainment) +
            (co7.po5 * co7_attainment),
            co1.po5 + co2.po5 + co3.po5 + co4.po5 + co5.po5 + co6.po5 + co7.po5
        )
        po6 = safe_division(
            (co1.po6 * co1_attainment) + (co2.po6 * co2_attainment) + (co3.po6 * co3_attainment) +
            (co4.po6 * co4_attainment) + (co5.po6 * co5_attainment) + (co6.po6 * co6_attainment) +
            (co7.po6 * co7_attainment),
            co1.po6 + co2.po6 + co3.po6 + co4.po6 + co5.po6 + co6.po6 + co7.po6
        )
        po7 = safe_division(
            (co1.po7 * co1_attainment) + (co2.po7 * co2_attainment) + (co3.po7 * co3_attainment) +
            (co4.po7 * co4_attainment) + (co5.po7 * co5_attainment) + (co6.po7 * co6_attainment) +
            (co7.po7 * co7_attainment),
            co1.po7 + co2.po7 + co3.po7 + co4.po7 + co5.po7 + co6.po7 + co7.po7
        )
        po8 = safe_division(
            (co1.po8 * co1_attainment) + (co2.po8 * co2_attainment) + (co3.po8 * co3_attainment) +
            (co4.po8 * co4_attainment) + (co5.po8 * co5_attainment) + (co6.po8 * co6_attainment) +
            (co7.po8 * co7_attainment),
            co1.po8 + co2.po8 + co3.po8 + co4.po8 + co5.po8 + co6.po8 + co7.po8
        )
        po9 = safe_division(
            (co1.po9 * co1_attainment) + (co2.po9 * co2_attainment) + (co3.po9 * co3_attainment) +
            (co4.po9 * co4_attainment) + (co5.po9 * co5_attainment) + (co6.po9 * co6_attainment) +
            (co7.po9 * co7_attainment),
            co1.po9 + co2.po9 + co3.po9 + co4.po9 + co5.po9 + co6.po9 + co7.po9
        )
        po10 = safe_division(
            (co1.po10 * co1_attainment) + (co2.po10 * co2_attainment) + (co3.po10 * co3_attainment) +
            (co4.po10 * co4_attainment) + (co5.po10 * co5_attainment) + (co6.po10 * co6_attainment) +
            (co7.po10 * co7_attainment),
            co1.po10 + co2.po10 + co3.po10 + co4.po10 + co5.po10 + co6.po10 + co7.po10
        )
        po11 = safe_division(
            (co1.po11 * co1_attainment) + (co2.po11 * co2_attainment) + (co3.po11 * co3_attainment) +
            (co4.po11 * co4_attainment) + (co5.po11 * co5_attainment) + (co6.po11 * co6_attainment) +
            (co7.po11 * co7_attainment),
            co1.po11 + co2.po11 + co3.po11 + co4.po11 + co5.po11 + co6.po11 + co7.po11
        )
        po12 = safe_division(
            (co1.po12 * co1_attainment) + (co2.po12 * co2_attainment) + (co3.po12 * co3_attainment) +
            (co4.po12 * co4_attainment) + (co5.po12 * co5_attainment) + (co6.po12 * co6_attainment) +
            (co7.po12 * co7_attainment),
            co1.po12 + co2.po12 + co3.po12 + co4.po12 + co5.po12 + co6.po12 + co7.po12
        )
        pso1 = safe_division(
            (co1.pso1 * co1_attainment) + (co2.pso1 * co2_attainment) + (co3.pso1 * co3_attainment) +
            (co4.pso1 * co4_attainment) + (co5.pso1 * co5_attainment) + (co6.pso1 * co6_attainment) +
            (co7.pso1 * co7_attainment),
            co1.pso1 + co2.pso1 + co3.pso1 + co4.pso1 + co5.pso1 + co6.pso1 + co7.pso1
        )
        pso2 = safe_division(
            (co1.pso2 * co1_attainment) + (co2.pso2 * co2_attainment) + (co3.pso2 * co3_attainment) +
            (co4.pso2 * co4_attainment) + (co5.pso2 * co5_attainment) + (co6.pso2 * co6_attainment) +
            (co7.pso2 * co7_attainment),
            co1.pso2 + co2.pso2 + co3.pso2 + co4.pso2 + co5.pso2 + co6.pso2 + co7.pso2
        )
        pso3 = safe_division(
            (co1.pso3 * co1_attainment) + (co2.pso3 * co2_attainment) + (co3.pso3 * co3_attainment) +
            (co4.pso3 * co4_attainment) + (co5.pso3 * co5_attainment) + (co6.pso3 * co6_attainment) +
            (co7.pso3 * co7_attainment),
            co1.pso3 + co2.pso3 + co3.pso3 + co4.pso3 + co5.pso3 + co6.pso3 + co7.pso3
        )
        pso4 = safe_division(
            (co1.pso4 * co1_attainment) + (co2.pso4 * co2_attainment) + (co3.pso4 * co3_attainment) +
            (co4.pso4 * co4_attainment) + (co5.pso4 * co5_attainment) + (co6.pso4 * co6_attainment) +
            (co7.pso4 * co7_attainment),
            co1.pso4 + co2.pso4 + co3.pso4 + co4.pso4 + co5.pso4 + co6.pso4 + co7.pso4
        )

    if num_co == 0:
        po1 = 0 
        po2 = 0 
        po3 = 0 
        po4 = 0 
        po5 = 0 
        po6 = 0 
        po7 = 0 
        po8 = 0 
        po9 = 0 
        po10 = 0 
        po11 = 0 
        po12 = 0 
        pso1 = 0 
        pso2 = 0 
        pso3 = 0 
        pso4 = 0 

    
    po1 = round(po1 ,2)
    po2 = round(po2 ,2)
    po3 = round(po3 ,2)
    po4 = round(po4 ,2)
    po5 = round(po5 ,2)
    po6 = round(po6 ,2)
    po7 = round(po7 ,2)
    po8 = round(po8 ,2)
    po9 = round(po9 ,2)
    po10 = round(po10 ,2)
    po11 = round(po11 ,2)
    po12 = round(po12 ,2)
    pso1 = round(pso1 ,2)
    pso2 = round(pso2 ,2)
    pso3 = round(pso3 ,2)
    pso4 = round(pso4 ,2)

    
    context = {
        'co1_attainment' :co1_attainment,
        'co2_attainment' :co2_attainment,
        'co3_attainment' :co3_attainment,
        'co4_attainment' :co4_attainment,
        'co5_attainment' :co5_attainment,
        'co6_attainment' :co6_attainment,
        'co7_attainment' :co7_attainment,
        'po1' : po1,
        'po2' : po2,
        'po3' : po3,
        'po4' : po4,
        'po5' : po5,
        'po6' : po6,
        'po7' : po7,
        'po8' : po8,
        'po9' : po9,
        'po10' : po10,
        'po11' : po11,
        'po12' : po12,
        'pso1' : pso1,
        'pso2' : pso2,
        'pso3' : pso3,
        'pso4' : pso4,
    }
    return render(request, 'myapp/calculate.html', context)
