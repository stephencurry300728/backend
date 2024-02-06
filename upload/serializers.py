from rest_framework import serializers
from .models import Assessment_Base

class AssessmentBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessment_Base
        fields = '__all__'