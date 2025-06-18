from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=Teacher)
def create_or_update_related_teacher_data(sender, instance, created, **kwargs):
    # Handle creation
    if created:
        # Create or update NumberOfCO instance
        NumberOfCO.objects.create(subject_name=instance.subject_name)

        # Create Questions instance
        Questions.objects.create(subject_name=instance.subject_name)

        # Create CO1-CO7 instances
        CO1.objects.create(subject_name=f"{instance.subject_name}")
        CO2.objects.create(subject_name=f"{instance.subject_name}")
        CO3.objects.create(subject_name=f"{instance.subject_name}")
        CO4.objects.create(subject_name=f"{instance.subject_name}")
        CO5.objects.create(subject_name=f"{instance.subject_name}")
        CO6.objects.create(subject_name=f"{instance.subject_name}")
        CO7.objects.create(subject_name=f"{instance.subject_name}")

        # Update Marks table for existing students
        students = Student.objects.all()
        for student in students:
            Marks.objects.create(
                subject_name=instance.subject_name,
                student_name=student.student_name,
                roll_number=student.roll_number,
            )
    else:
        # Handle updates
        # Update or create NumberOfCO instance
        NumberOfCO.objects.update_or_create(
            subject_name=instance.subject_name,
            defaults={"subject_name": instance.subject_name},
        )

        # Update or create Questions instance
        Questions.objects.update_or_create(
            subject_name=instance.subject_name,
            defaults={"subject_name": instance.subject_name},
        )

        # Update or create CO1-CO7 instances
        for co_class in [CO1, CO2, CO3, CO4, CO5, CO6, CO7]:
            co_class.objects.update_or_create(
                subject_name=f"{instance.subject_name}",
                defaults={"subject_name": instance.subject_name},
            )

        # Update Marks table for existing students
        students = Student.objects.all()
        for student in students:
            Marks.objects.update_or_create(
                subject_name=instance.subject_name,
                student_name=student.student_name,
                roll_number=student.roll_number,
                defaults={
                    "subject_name": instance.subject_name,
                    "student_name": student.student_name,
                    "roll_number": student.roll_number,
                },
            )

@receiver(post_delete, sender=Teacher)
def delete_related_teacher_data(sender, instance, **kwargs):
    # Delete related entries in NumberOfCO, Questions, CO, and Marks
    NumberOfCO.objects.filter(subject_name=instance.subject_name).delete()
    Questions.objects.filter(subject_name=instance.subject_name).delete()
    CO1.objects.filter(subject_name=instance.subject_name).delete()
    CO2.objects.filter(subject_name=instance.subject_name).delete()
    CO3.objects.filter(subject_name=instance.subject_name).delete()
    CO4.objects.filter(subject_name=instance.subject_name).delete()
    CO5.objects.filter(subject_name=instance.subject_name).delete()
    CO6.objects.filter(subject_name=instance.subject_name).delete()
    CO7.objects.filter(subject_name=instance.subject_name).delete()
    Marks.objects.filter(subject_name=instance.subject_name).delete()

    
@receiver(post_save, sender=Student)
def create_or_update_marks_for_student(sender, instance, created, **kwargs):
    # Retrieve all existing subjects from Teacher model
    subjects = Teacher.objects.values_list('subject_name', flat=True)

    if created:
        # Add entries in Marks table for all subjects when a new student is created
        for subject in subjects:
            Marks.objects.create(
                subject_name=subject,
                student_name=instance.student_name,
                roll_number=instance.roll_number,
            )
    else:
        # Update entries in Marks table when a student is updated
        for subject in subjects:
            Marks.objects.update_or_create(
                subject_name=subject,
                student_name=instance.student_name,
                defaults={"roll_number": instance.roll_number},
            )


@receiver(post_delete, sender=Student)
def delete_marks_for_deleted_student(sender, instance, **kwargs):
    # Delete all marks entries for the deleted student
    Marks.objects.filter(roll_number=instance.roll_number).delete()



