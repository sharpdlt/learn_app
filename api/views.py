from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Course, Group, Student
from api.serializers import CourseSerializer


class CourseList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user.id
        student = Student.objects.get(user_id=user)
        group = Group.objects.get(pk=student.group_id)
        course = Course.objects.get(pk=group.course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
