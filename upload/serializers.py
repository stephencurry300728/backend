from rest_framework import serializers
from .models import Assessment_Base

class AssessmentBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessment_Base
        fields = '__all__'  # 包括所有基础字段加上'assessment_detail_url'