from rest_framework import serializers



from .models import Job,Skill
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
       
            'location',
           
            'job_type',  # Include if your Job model has it
            'skills',    # Include if your Job model has a ManyToManyField
            'status',    # Read-only; admin verifies later
            'created_at'
        ]
        read_only_fields = ['status', 'created_at', 'company']

    def create(self, validated_data):
        # Automatically attach the company from request context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['company'] = request.user
        return super().create(validated_data)
# class PublicJobSerializer(serializers.ModelSerializer):
#     company_name = serializers.CharField(
#         source="company.full_name",
#         read_only=True
#     )

#     class Meta:
#         model = Job
#         fields = [
#             'id',
#             'title',
#             'company_name',
#             'location',
#             'salary',
#             'created_at'
#         ]

class PublicJobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.full_name",
        read_only=True
    )
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'company_name',
            'job_type',
            'location',
            'skills',
            'created_at'
        ]
# class CompanyJobCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Job
#         fields = [
#             'id',
#             'title',
         
#             'location',
        
#             'job_type',  # include if your Job model has job_type
#             'skills',    # include if your Job model has ManyToManyField skills
#             'status',    # read-only, admin verifies
#             'created_at',
#         ]
#         read_only_fields = ['status', 'created_at', 'company']
# class CompanyJobCreateSerializer(serializers.ModelSerializer):
#     skills = serializers.SlugRelatedField(
#         many=True,
#         slug_field='name',
#         queryset=Skill.objects.all()
#     )

#     class Meta:
#         model = Job
#         fields = ['title', 'location', 'job_type', 'skills']

#     def create(self, validated_data):
#         request = self.context.get('request')
#         if request and hasattr(request, 'user'):
#             validated_data['company'] = request.user  # Attach logged-in company
#         return super().create(validated_data)
class CompanyJobCreateSerializer(serializers.ModelSerializer):
    skills = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Job
        fields = ['title', 'job_type', 'location', 'skills']

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        job = Job.objects.create(**validated_data)
        for skill_name in skills_data:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            job.skills.add(skill)
        return job
