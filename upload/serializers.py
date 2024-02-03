from rest_framework import serializers
from django.urls import reverse
from .models import Assessment_Base, Assessment_09A02, Assessment_09A0304, Assessment_10A01, Assessment_10A02

# class AssessmentBaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Assessment_Base
#         fields = '__all__'

class AssessmentBaseSerializer(serializers.ModelSerializer):
    # 获取司机基本信息后，返回该（特地Id）司机在另外一张模型中考评数据的url
    assessment_detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Assessment_Base
        fields = '__all__'  # 包括所有基础字段加上'assessment_detail_url'

    '''
    当从数据库查询Assessment_Base对象并通过AssessmentBaseSerializer进行序列化时
    每个对象实例都会被传递给get_assessment_detail_url 函数以生成相应的URL
    reverse函数用于根据URL的名称和可选的参数来反向解析URL,主路由中的basename
    -detail 后缀明确表示这个URL是用来访问资源的详细信息的，以此区分列表视图（显示资源集合）和详细视图（显示单个资源的详情）
    一般 basename will be automatically generated based on the queryset attribute of the viewset,这里方便后续reverse
    '''
    # 动态生成指向特定车型驾驶员测评的详细信息页面的URL
    def get_assessment_detail_url(self, obj):
        # obj参数：当前正在被序列化的Assessment_Base模型实例
        request = self.context.get('request')
        if hasattr(obj, 'assessment_09A02'):
            # 通过 HttpRequest对象的实例, build_absolute_uri方法：构建一个完整的URL,
            return request.build_absolute_uri(reverse('assessment09a02-detail', args=[obj.assessment_09A02.pk]))
        elif hasattr(obj, 'assessment_09A0304'):
            return request.build_absolute_uri(reverse('assessment09a0304-detail', args=[obj.assessment_09A0304.pk]))
        elif hasattr(obj, 'assessment_10A01'):
            return request.build_absolute_uri(reverse('assessment10a01-detail', args=[obj.assessment_10A01.pk]))
        elif hasattr(obj, 'assessment_10A02'):
            return request.build_absolute_uri(reverse('assessment10a02-detail', args=[obj.assessment_10A02.pk]))
        return None


# 确保了每种车型详细信息的API响应能包含所有相关字段
class Assessment09A02Serializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_09A02
        fields = '__all__' # 哪些模型字段会被包含在API响应中

class Assessment09A0304Serializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_09A0304
        fields = '__all__'

class Assessment10A01Serializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_10A01
        fields = '__all__'

class Assessment10A02Serializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_10A02
        fields = '__all__'