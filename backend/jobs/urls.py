from django.urls import path
from .views import (
    CompanyJobCreateView,
    CompanyJobListView,
    CompanyJobDetailView,
    AdminJobListView,
    AdminJobVerifyView,
    PublicJobListView,
    JobUpdateView, 
    JobDeleteView

)

urlpatterns = [
    path('company/jobs/', CompanyJobListView.as_view()),
    path('company/jobs/create/', CompanyJobCreateView.as_view()),
    path('company/jobs/<int:pk>/', CompanyJobDetailView.as_view()),
     path('job/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('job/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('admin/jobs/', AdminJobListView.as_view()),
    path('admin/jobs/<int:pk>/verify/', AdminJobVerifyView.as_view()),
     path('jobs/', PublicJobListView.as_view()),

    # path('jobs/<int:pk>/', PublicJobDetailView.as_view()),
]
