from django.urls import path
from .views import (
    CompanyJobCreateView,
    CompanyJobListView,
    CompanyJobDetailView
)

urlpatterns = [
    path('company/jobs/', CompanyJobListView.as_view()),
    path('company/jobs/create/', CompanyJobCreateView.as_view()),
    path('company/jobs/<int:pk>/', CompanyJobDetailView.as_view()),
]
