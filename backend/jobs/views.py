from django.shortcuts import render

# Create your views here.
from rest_framework import generics,permissions
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer,PublicJobSerializer,AdminJobSerializer,CompanyJobCreateSerializer
from .permissions import IsCompany, IsOwnerCompany


from .permissions import IsAdminUserRole
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class AdminJobListView(generics.ListAPIView):
    serializer_class = AdminJobSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_queryset(self):
        queryset = Job.objects.select_related('company')

        status = self.request.query_params.get('status')
        company = self.request.query_params.get('company')

        if status:
            queryset = queryset.filter(status=status)

        if company:
            queryset = queryset.filter(company__email=company)

        return queryset



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

class AdminJobVerifyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def patch(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response(
                {"detail": "Job not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        action = request.data.get("action")

        if action == "approve":
            job.status = "approved"
        elif action == "reject":
            job.status = "rejected"
        else:
            return Response(
                {"detail": "Invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )

        job.save()
        return Response(
            {
                "message": f"Job {action}d successfully",
                "status": job.status
            }
        )

class PublicJobListView(generics.ListAPIView):
    serializer_class = PublicJobSerializer

    def get_queryset(self):
        queryset = Job.objects.filter(status='approved')

        job_type = self.request.query_params.get('job_type')
        location = self.request.query_params.get('location')
        skill = self.request.query_params.get('skill')

        if job_type:
            queryset = queryset.filter(job_type=job_type)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if skill:
            queryset = queryset.filter(skills__name__icontains=skill)

        return queryset.distinct()

class CompanyJobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = CompanyJobCreateSerializer
    permission_classes = [permissions.IsAuthenticated]  


class JobUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany, IsOwnerCompany]

# Delete Job listing
class JobDeleteView(generics.DestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany, IsOwnerCompany]