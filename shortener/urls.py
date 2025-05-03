from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),  # Root URL pattern
    #path('shorten/', views.CreateShortURL.as_view()),
    #path('shorten/<str:shortcode>/', views.RetrieveOriginalURL.as_view()),
    #path('shorten/<str:shortcode>/update/', views.UpdateShortURL.as_view()),
    #path('shorten/<str:shortcode>/delete/', views.DeleteShortURL.as_view()),
    #path('shorten/<str:shortcode>/stats/', views.GetStatistics.as_view()),
    #path('<str:shortcode>/', views.redirect_view),
] 