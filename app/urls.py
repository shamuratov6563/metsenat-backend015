from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentListAPIView.as_view()),
    path('students/<int:pk>', views.StudentDetailAPIView.as_view()),
    path('student-sponsor-create/', views.StudentSponsorCreateAPIView.as_view()),
    path('student-sponsors/', views.StudentSponsorListAPIView.as_view()),
    path('amount-statistic/', views.StatisticAPIView.as_view()),
    path('graphic/', views.GraphicAPIView.as_view())
]