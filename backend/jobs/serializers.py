from rest_framework import serializers
from .models import Job

from rest_framework import serializers
from .models import Job

class AdminJobSerializer(serializers.ModelSerializer):
    company_email = serializers.CharField(
        source='company.email',
        read_only=True
    )

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'company_email',
            'location',
            'salary',
            'status',
            'created_at'
        ]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'location',
            'salary',
            'status',
            'created_at'
        ]
        read_only_fields = ['status', 'created_at']
