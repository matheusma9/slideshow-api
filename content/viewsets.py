from rest_framework import status
from .serializers import GroupSerializer, ContentSerializer, MediaSerializer
from .models import Group, Content, Media
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from utils.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.fields import get_fields
from django.utils import dateparse
from django.db.models import F
from utils.schema_view import CustomSchema
from utils.models import Log
from utils import viewsets


class GroupViewset(viewsets.ModelViewSet):
    """

    Endpoint relacionado aos grupos.

    """
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    schema = CustomSchema()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(methods=['post'], detail=True)
    def add(self, request, pk):
        """
        ---
        method_path:
         /groups/{id}/add/
        method_action:
         POST
        desc:
         Adicionar conteúdo no grupo.
        input:
        - name: media
          desc: Id da mídia.
          type: integer
          required: True
          location: form
        - name: duration
          desc: Duração da exibição
          type: str
          required: True
          location: form
        """
        group = self.get_object()
        media_pk, duration = get_fields(request.data, ['media', 'duration'])
        media = get_object_or_404(Media, pk=media_pk)
        content = Content.objects.create(media=media, duration=dateparse.parse_duration(duration), group=group, order=group.group_contents.count() + 1)
        Log.objects.create(user=request.user, action='create', content_object=content)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    
    @action(methods=['patch'], detail=True)
    def up(self, request, pk):
        """
        ---
        method_path:
         /groups/{id}/up/
        method_action:
         PATCH
        desc:
         Aumentar a ordem do conteúdo
        input:
        - name: content
          desc: Id do conteúdo 
          type: integer
          required: True
          location: form
        """
        group = self.get_object()
        content_pk, *_ = get_fields(request.data, ['content'])
        content = get_object_or_404(Content, pk=content_pk)
        if content.order > 1:
            group.group_contents.filter(order=content.order-1).update(order=content.order)
            content.order -= 1
            content.save()
            Log.objects.create(user=request.user, action='update', content_object=content)
        serializer = self.get_serializer(group)
        return Response(serializer.data)
    
    @action(methods=['patch'], detail=True)
    def down(self, request, pk):
        """
        ---
        method_path:
         /groups/{id}/down/
        method_action:
         PATCH
        desc:
         Diminuir a ordem do conteúdo
        input:
        - name: content
          desc: Id do conteúdo 
          type: integer
          required: True
          location: form
        """
        group = self.get_object()
        content_pk, *_ = get_fields(request.data, ['content'])
        content = get_object_or_404(Content, pk=content_pk)
        
        if content.order < group.group_contents.count():
            group.group_contents.filter(order=content.order+1).update(order=content.order)
            content.order += 1
            content.save()
            Log.objects.create(user=request.user, action='update', content_object=content)
        serializer = self.get_serializer(group)
        return Response(serializer.data)

    @action(methods=['delete'], detail=True, url_path=r'remove/(?P<content_pk>[0-9]+)')
    def remove(self, request, pk, content_pk):
        """
        ---
        method_path:
         /groups/{id}/remove/{content_pk}/
        method_action:
         DELETE
        desc:
         Remover o conteúdo do grupo.
        input:
        - name: content_pk
          desc: Id do conteúdo 
          type: integer
          required: True
          location: path
        """
        group = self.get_object()
        content = get_object_or_404(Content, pk=content_pk)

        group.group_contents.filter(order__gte=content.order+1).update(order=F('order') - 1)
        Log.objects.create(user=request.user, action='delete', content_object=content)
        content.delete()
        serializer = self.get_serializer(group)
        return Response(serializer.data)


class ContentViewset(viewsets.ModelViewSet):
    """
    Endpoint relacionado aos conteúdos.
    """
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class MediaViewset(viewsets.ModelViewSet):
    """
    Endpoint relacionado as mídias.
    """
    serializer_class = MediaSerializer
    queryset = Media.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    
