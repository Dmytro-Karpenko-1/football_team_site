from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('team/', views.team, name='team'),
    path('matches/', views.matches, name='matches'),
    path('standings/', views.standings, name='standings'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('join/', views.join, name='join'),
    path('sponsors/', views.sponsors, name='sponsors'),
]
