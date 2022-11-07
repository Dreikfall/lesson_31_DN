from django.urls import path

from ads import views

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('create/', views.AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/update/', views.AdUpdateView.as_view()),
    path('<int:pk>/delete/', views.AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', views.AdImageView.as_view()),
]