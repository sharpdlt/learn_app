from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .utilities import get_timestamp_path
from .apps import user_registered

from .apps import user_registered


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(models.Model):
    course_name = models.CharField(max_length=128)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to=get_timestamp_path)

    def __str__(self) -> str:
        return self.course_name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Group(models.Model):
    group_name = models.CharField(max_length=64)
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.course.course_name} - {self.group_name}'

    class Meta:
        verbose_name_plural = 'Группы'
        verbose_name = 'Группа'


class Subject(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT)
    subject_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.subject_name} - {self.course.course_name}'

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Header(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    header_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.header_name} - {self.subject.subject_name}'

    class Meta:
        verbose_name = 'Глава'
        verbose_name_plural = 'Главы'


class Topic(models.Model):
    header = models.ForeignKey(Header, on_delete=models.PROTECT)
    topic_name = models.CharField(max_length=255)
    content = models.TextField()
    duration = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.topic_name} - {self.header.header_name}'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Role(models.Model):
    ADMIN = 0
    SUPERVISOR = 1
    MANAGER = 2
    TEACHER = 3
    STUDENT = 4
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (SUPERVISOR, 'supervisor'),
        (MANAGER, 'manager'),
        (TEACHER, 'teacher'),
        (STUDENT, 'student'),
    )
    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, primary_key=True)

    def __str__(self) -> str:
        return self.get_id_display()

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class Profile(AbstractUser):
    roles = models.ManyToManyField(Role)
    date_of_birth = models.DateField(
        blank=True, null=True)
    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(
        validators=[phone_number_regex], max_length=16, unique=True,
        blank=True, null=True)
    phone_number_alt = models.CharField(
        validators=[phone_number_regex], max_length=16, unique=True,
        blank=True, null=True)
    address = models.CharField(blank=True, max_length=256)
    image = models.ImageField(
        blank=True, upload_to=get_timestamp_path)
    is_activated = models.BooleanField(
        default=False, db_index=True)
    is_active = models.BooleanField(default=False)
    resume_addr = models.URLField(
        blank=True, max_length=200)
    portfolio_addr = models.URLField(
        blank=True, max_length=200)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        user_registered.send(Profile, instance=self)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Student(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, on_delete=models.PROTECT)
    rating = models.FloatField(default=0)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
