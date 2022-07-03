import datetime
from django.contrib import admin

from .models import Course, Subject, Group, Topic, Header
from .models import Profile, Role, Teacher, Student
from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


send_activation_notifications.short_description = 'Отправка писем с требованиями активации'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (
        ('first_name', 'last_name'),
        ('username', 'email'),
        ('is_active', 'is_activated'),
        'roles',
        'date_of_birth', 'phone_number',
        'phone_number_alt', 'address',
        'resume_addr', 'portfolio_addr', 'image',
    )
    readonly_fields = ('last_login', 'date_joined',)
    actions = [send_activation_notifications, ]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Role)
admin.site.register(Group)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Header)
admin.site.register(Topic)
