from django.conf.urls import url
from django.urls import path, include

import quiz.views as quiz_views
from . import views
app_name = "quiz"
urlpatterns = [


	path("", views.home, name="home"),
	#path("questions/", views.qpage, name="questions"),
	path("create-quiz", views.createQuiz, name="create-quiz"),
	path("create-question", views.createQuestions, name="create-question"),
	path("quizzes", views.quizzes, name="quizzes"),
	path("results", views.results, name="results"),
	path("answers", views.attemptquiz, name="answers"),
	path("quizzes/<int:id>", views.attemptquiz, name="attempt-quiz"),
	path("results/<int:id>", views.result, name="quiz-result"),
 
	# 
     # _____________ Answer URLs__________________#
    url(r'^api/answer$', views.AnswerModel_list),
    url(r'^api/answer/(?P<pk>[0-9]+)$', views.AnswerModel_detail),
    # url(r'^api/answer/published$', views.AnswerModel_list_active),
	
     # _____________ Question URLs__________________#
    url(r'^api/question$', views.QuesModel_list),
    url(r'^api/question/(?P<pk>[0-9]+)$', views.QuesModel_detail),
    # url(r'^api/answer/published$', views.AnswerModel_list_active),
	
     # _____________ Quiz URLs__________________#
    url(r'^api/quiz$', views.QuizModel_list),
    url(r'^api/quiz/(?P<pk>[0-9]+)$', views.QuizModel_detail),
    # url(r'^api/answer/published$', views.AnswerModel_list_active),
	
     # _____________ Result URLs__________________#
    url(r'^api/result$', views.ResultModel_list),
    url(r'^api/result/(?P<pk>[0-9]+)$', views.ResultModel_detail),
    # url(r'^api/answer/published$', views.AnswerModel_list_active),
	


]
