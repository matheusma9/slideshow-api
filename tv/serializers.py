from rest_framework import serializers
from .models import TV
from content.serializers import ContentSerializer

class TVSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedRelatedField( view_name='group-detail', read_only=True)
    preview = ContentSerializer(read_only=True)

    class Meta:
        model = TV
        fields = ['id','name', 'group', 'preview']
