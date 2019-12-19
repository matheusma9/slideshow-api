from rest_framework import serializers
from .models import Media, Content, Group

class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ['id', 'name', 'source', 'ftype']
        read_only_fields = ['id']

class ContentSerializer(serializers.ModelSerializer):
    media = MediaSerializer()

    class Meta:
        model = Content
        fields = ['id', 'duration', 'media', 'order']
        read_only_fields = ['id']


class ContentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ['id', 'duration', 'media', 'order']
        read_only_fields = ['id']

class GroupSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, source='group_contents', required=False)

    class Meta:
        model = Group
        fields = ['id', 'name', 'contents']
        read_only_fields = ['id']