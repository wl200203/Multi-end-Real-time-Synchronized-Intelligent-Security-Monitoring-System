from rest_framework import serializers
from .models import Post  # 确保存在名为 Post 的模型

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  # 或者指定需要序列化的字段