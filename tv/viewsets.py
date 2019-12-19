from utils import viewsets
from .serializers import TVSerializer
from .models import TV
from utils.fields import get_fields
from utils.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from content.models import Group
from utils.schema_view import CustomSchema
from utils.models import Log
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TVViewset(viewsets.ModelViewSet):
    """
    Endpoint relacionado as tvs.
    """
    serializer_class = TVSerializer
    queryset = TV.objects.all()
    schema = CustomSchema()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """
        ---
        method_path:
         /tvs/
        method_action:
         GET
        desc:
         Adicionar grupo na tv.
        input:
        - name: tipo
          desc: Tipo de acesso(admin ou tv).
          type: string
          required: False
          location: query
        """
        tipo = request.GET.get('tipo', 'tv')
        if tipo == 'tv':
          queryset = self.get_queryset().filter(group__isnull=False)
        else:
          queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def add(self, request, pk):
        """
        ---
        method_path:
         /tvs/{id}/add/
        method_action:
         POST
        desc:
         Adicionar grupo na tv.
        input:
        - name: group
          desc: Id do grupo.
          type: integer
          required: True
          location: form
        """
        tv = self.get_object()
        group_pk, *_ = get_fields(request.data, ['group'])
        group = get_object_or_404(Group, pk=group_pk) 
        tv.group = group
        tv.save()
        serializer = self.get_serializer(tv)
        Log.objects.create(user=request.user, action='update', content_object=tv)
        return Response(serializer.data)