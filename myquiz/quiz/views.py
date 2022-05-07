from django.shortcuts import redirect, render
from .models import *
from .forms import *
# Serializer imports
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from quiz .models import QuesModel
from quiz .models import QuizModel
from quiz .models import ResultModel
from quiz .models import AnswerModel
from quiz .serializers import QuesModelSerializer
from quiz .serializers import QuizModelSerializer
from quiz .serializers import ResultModelSerializer
from quiz .serializers import AnswerModelSerializer


# Create your views here.
def home(request):

    return render(request, 'index.html')


def createQuiz(request):
    form = addQuizform()
    if request.method == 'POST':
        form = addQuizform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/create-question')
    context = {'form': form}
    return render(request, 'addquiz.html', context)


def createQuestions(request):
    form = addQuestionform()
    if request.method == 'POST':
        form = addQuestionform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'addquestion.html', context)


'''
def qpage(request):
    questions = QuesModel.objects.all()
    dict: questions
    if (request.method == 'POST'):
        print(request.POST.dict())
    return render(request, 'quiz.html', {'questions': questions})'''


def quizzes(request):
    quizzes = QuizModel.objects.all()

    return render(request, 'quizzes.html', {'quizzes': quizzes})


def results(request):
    quizzes = QuizModel.objects.all()

    return render(request, 'Results.html', {'quizzes': quizzes})



def generateresult(id):

    answers = AnswerModel.objects.filter(Question_ID__Quiz_ID=id)
    quiz_id = QuizModel.objects.get(Quiz_ID=id)
    correct = 0
    incorrect = 0

    for i in answers:
        if i.isCorrect:
            correct += 1
        else:
            incorrect += 1


    res = ResultModel(Quiz_ID=quiz_id, Marks=correct)
    res.save()

def attemptquiz(request, id):
    questions = QuesModel.objects.filter(Quiz_ID=id)
    # dict = request.POST.dict()
    if request.method == 'POST':
        dict = request.POST.dict()
        dict.pop('csrfmiddlewaretoken')
        # print(dict.items())

        for k, v in dict.items():
            q_id = QuesModel.objects.get(id=k)
            is_correct = q_id.answer == v
            print(is_correct)

            ans = AnswerModel(Question_ID=q_id, Answer=v, isCorrect=is_correct)
            ans.save()

        answers = AnswerModel.objects.all()

        generateresult(id)

        return render(request, 'answers.html', {'answers': answers})

    return render(request, 'quiz.html', {'questions': questions})


def result(request, id):
    quiz_id = QuizModel.objects.get(Quiz_ID=id)
    results = ResultModel.objects.filter(Quiz_ID=quiz_id)

    if results.exists():
        print('yes', results)

        return render(request, 'result.html', {'results': results})

    else:
        message = 'You havent attempted this quiz yet'
        return render(request, 'result.html', {'message': message})

    return render(request, 'result.html', {'results': results})




# __________________ Serializer View setting ____________________#

# ___________________________________________________________________________________________________________________


#________________For Quiz Model ____________________#

@api_view(['GET', 'POST', 'DELETE'])
def QuizModel_list(request):
    if request.method == 'GET':
        tutorials = QuizModel.objects.all()
        
        title = request.query_params.get('Quiz_name', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = QuizModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = QuizModelSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = QuizModel.objects.all().delete()
        return JsonResponse({'message': '{} QuizModel were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def QuizModel_detail(request, pk):
    try: 
        tutorial = QuizModel.objects.get(pk=pk) 
    except QuizModel.DoesNotExist: 
        return JsonResponse({'message': 'The QuizModel does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = QuizModelSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = QuizModelSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'QuizModel was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def QuizModel_list_active(request):
    tutorials = QuizModel.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = QuizModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#QuizModel part ended here
    
    #________________For QuesModel____________________#

@api_view(['GET', 'POST', 'DELETE'])
def QuesModel_list(request):
    if request.method == 'GET':
        tutorials = QuesModel.objects.all()
        
        title = request.query_params.get('Quiz_ID', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = QuesModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = QuesModelSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = QuesModel.objects.all().delete()
        return JsonResponse({'message': '{} QuesModel were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def QuesModel_detail(request, pk):
    try: 
        tutorial = QuesModel.objects.get(pk=pk) 
    except QuesModel.DoesNotExist: 
        return JsonResponse({'message': 'The QuesModel does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = QuesModelSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = QuesModelSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'QuesModel was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def QuesModel_list_active(request):
    tutorials = QuesModel.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = QuesModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#QuesModel part ended here
    
    #________________For ResultModel ____________________#

@api_view(['GET', 'POST', 'DELETE'])
def ResultModel_list(request):
    if request.method == 'GET':
        tutorials = ResultModel.objects.all()
        
        title = request.query_params.get('Quiz_ID', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = ResultModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = ResultModelSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = ResultModel.objects.all().delete()
        return JsonResponse({'message': '{} ResultModel were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def ResultModel_detail(request, pk):
    try: 
        tutorial = ResultModel.objects.get(pk=pk) 
    except ResultModel.DoesNotExist: 
        return JsonResponse({'message': 'The ResultModel does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = ResultModelSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = ResultModelSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'ResultModel was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def ResultModel_list_active(request):
    tutorials = ResultModel.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = ResultModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#ResultModel part ended here
    
    #________________For Answer____________________#

@api_view(['GET', 'POST', 'DELETE'])
def AnswerModel_list(request):
    if request.method == 'GET':
        tutorials = AnswerModel.objects.all()
        
        title = request.query_params.get('Answer_ID', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = AnswerModelSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = AnswerModelSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = AnswerModel.objects.all().delete()
        return JsonResponse({'message': '{} AnswerModel were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def AnswerModel_detail(request, pk):
    try: 
        tutorial = AnswerModel.objects.get(pk=pk) 
    except AnswerModel.DoesNotExist: 
        return JsonResponse({'message': 'The AnswerModel does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = AnswerModelSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = AnswerModelSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'AnswerModel was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
# @api_view(['GET'])
# def AnswerModel_list_active(request):
#     tutorials = AnswerModel.objects.filter(published=True)
        
#     if request.method == 'GET': 
#         tutorials_serializer = AnswerModelSerializer(tutorials, many=True)
#         return JsonResponse(tutorials_serializer.data, safe=False)
    
    #__________________________________________________________#AnswerModel part ended here
    
    
