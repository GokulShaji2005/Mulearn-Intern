from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer
from .permissions import IsCompany, IsOwnerCompany

class CompanyJobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsCompany]

    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user,
            status='pending'
        )

class CompanyJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsCompany]

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user)
class CompanyJobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [
        IsAuthenticated,
        IsCompany,
        IsOwnerCompany
    ]

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user)
