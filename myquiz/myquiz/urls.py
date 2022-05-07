from django.conf.urls import url, include
from django.contrib import admin

from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from courses import views


urlpatterns = [

    path('', include('users.urls')),
	path('', include('quiz.urls')),
    path('', include('assignment.urls')),
    path('', include('announcements.urls')),
    # path(r'^courses/', include('course.url')),
    path('api-auth/', include('rest_framework.urls')),

    url(r'^admin/', admin.site.urls),
    # ####
    # url(r'^courses/', views.courselist.as_view()),
    # ####
    url(r'^', include('courses.urls')),
]

