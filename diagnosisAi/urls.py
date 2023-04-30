from django.urls import path
from . import views
urlpatterns=[
  path('heart_analysis',views.HeartAnalysis.as_view()),
  path('liver_analysis',views.LiverAnalysis.as_view()),
]