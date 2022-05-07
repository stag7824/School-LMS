# from django.shortcuts import render

# # Create your views here.
# from rest_framework import status
 
# from rest_framework.decorators import api_view
 
# from rest_framework.response import Response
 
# from courses .models import Course
 
# from courses .serializers import CourseSerializer

# # @api_view([‘GET’, ‘POST’])
# @api_view(['GET', 'POST'])
# def course_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     sad
#     """
    
#     if request.method == 'GET':
#         courses = Course.objects.all()
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

 
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from courses .models import Course
from courses .models import Enrollment
from courses .serializers import CourseSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from courses .serializers import EnrollmentSerializer


# works

# class courselist(APIView):
#     def get(self, request):
#         course1=Course.objects.all()
#         serialzer=CourseSerializer(course1,many=True)
#         return Response(serialzer.data)
#         # pass
    
#     def post(self,request):
#         serialzer=CourseSerializer(data=request.data)
#         if serialzer.is_valid():
#             serialzer.save()
#             return Response(serialzer.data, status=status.HTTP_201_CREATED)
#         return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request):
#         Course.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# _____________________________________________


# @api_view( ['GET', 'PUT', 'DELETE'])
# def courselist(request, pk):
#     """[](C:\microsoft\pylance-release\blob\main\DIAGNOSTIC_SEVERITY_RULES.md)
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         Course1 = Course.objects.get(pk=pk)
#     except Course.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = CourseSerializer(Course1)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = CourseSerializer(Course1, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         Course1.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#________________For Courses____________________#

@api_view(['GET', 'POST', 'DELETE'])
def course_list(request):
    if request.method == 'GET':
        tutorials = Course.objects.all()
        
        title = request.query_params.get('course_name', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = CourseSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = CourseSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Course.objects.all().delete()
        return JsonResponse({'message': '{} Courses were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, pk):
    try: 
        tutorial = Course.objects.get(pk=pk) 
    except Course.DoesNotExist: 
        return JsonResponse({'message': 'The Course does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = CourseSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = CourseSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Course was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def course_list_active(request):
    tutorials = Course.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = CourseSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#Course part ended here
    
#________________Enrollment____________________#

@api_view(['GET', 'POST', 'DELETE'])
def enrollment_list(request):
    if request.method == 'GET':
        tutorials = Enrollment.objects.all()
        
        title = request.query_params.get('course', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = EnrollmentSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = EnrollmentSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Enrollment.objects.all().delete()
        return JsonResponse({'message': '{} Enrollment were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def enrollment_detail(request, pk):
    try: 
        tutorial = Enrollment.objects.get(pk=pk) 
    except Enrollment.DoesNotExist: 
        return JsonResponse({'message': 'The Enrollment does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = EnrollmentSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = EnrollmentSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Enrollment was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def Enrollment_list_active(request):
    tutorials = Enrollment.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = EnrollmentSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#Enrollment part ended here
    