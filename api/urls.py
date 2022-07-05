from django.urls import path
from api.views import CourseList, CourseDetail

app_name = 'api'

urlpatterns = [
    path('courses/', CourseList.as_view(), name='course-list'),
    path('courses/<int:pk>', CourseDetail.as_view(), name='course-detail    '),

]
