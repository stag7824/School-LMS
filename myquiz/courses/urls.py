from django.conf.urls import include, url
from django.urls import path
 
from django.contrib import admin
 
from  courses import views
 
urlpatterns = [
    # url(r'^api/', views.course_list),
    # url(r'^api/course_by_id/(?P<pk>[0-9]+)$', views.course_detail),
    
    ###############################################################
    url(r'^api/courses$', views.course_list),
    url(r'^api/courses/(?P<pk>[0-9]+)$', views.course_detail),
    url(r'^api/courses/published$', views.course_list_active)
]