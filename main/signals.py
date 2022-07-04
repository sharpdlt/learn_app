from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Student, Group, Teacher
from django.db import transaction


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


@receiver(post_save, sender=Profile)
@on_transaction_commit
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        for r in instance.roles.all():
            if str(r) == 'student':
                Student.objects.update_or_create(
                    user=instance, group=Group.objects.get(pk=1))
            if str(r) == 'teacher':
                Teacher.objects.update_or_create(user=instance)


@receiver(post_save, sender=Profile)
def save_user_profile(sender, instance, **kwargs):
    for r in instance.roles.all():
        if str(r) == 'student':
            Student.objects.update_or_create(
                user=instance, group=Group.objects.get(pk=1))
        if str(r) == 'teacher':
            Teacher.objects.update_or_create(user=instance)
