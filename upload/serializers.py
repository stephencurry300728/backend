from rest_framework import serializers
from .models import Assessment_Base

class AssessmentBaseSerializer(serializers.ModelSerializer):
    # 添加一个新的字段trainLines, 这个字段不在模型中定义，而是动态计算得到
    trainLines = serializers.SerializerMethodField()

    class Meta:
        model = Assessment_Base
        fields = '__all__'  # 确保包含所有模型字段以及新添加的trainLines字段

    # 定义一个方法来获取train_model字段的前两位
    def get_trainLines(self, obj):
        # 如果train_model字段存在且长度大于等于2, 则返回其前两位
        if obj.train_model and len(obj.train_model) >= 2:
            return obj.train_model[:2]
        return None  # 如果条件不满足，返回None或者一个默认值