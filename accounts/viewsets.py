from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .permission import IsOwnerOrCreateOnly
from utils.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from rest_framework import status
from utils.fields import get_fields
from django.conf import settings
from utils.schema_view import CustomSchema

class UserViewSet(viewsets.ModelViewSet):
    """
    Endpoint relacionado aos Usuários.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all() 
    permission_classes = [IsOwnerOrCreateOnly]
    schema = CustomSchema()

    @action(methods=['post'], detail=False)
    def solicitar(self, request):
        """
        ---
        method_path:
         /accounts/solicitar/
        method_action:
         POST
        desc:
         Solicitar alteração de senha.
        input:
        - name: email
          desc: Email do usuário.
          type: str
          required: True
          location: form
        """
        to_email, *_ = get_fields(request.data, ['email'])
        user = get_object_or_404(User, email=to_email)
        mail_subject = 'Solicitação para alteração de senha'
        message = render_to_string('accounts/pass_reset.html', {
            'user': user,
            'domain': settings.FRONT_END_HOST,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return Response({'message':'A solicitação será enviada para o seu email.'})
    
    @action(methods=['post'], detail=False)
    def reset(self, request):
        """
        ---
        method_path:
         /accounts/reset/
        method_action:
         POST
        desc:
         Alterar senha.
        input:
        - name: uid
          desc: Uid do usuário.
          type: str
          required: True
          location: form
        - name: token
          desc: token do usuário.
          type: str
          required: True
          location: form
        - name: password
          desc: Nova senha do usuário.
          type: str
          required: True
          location: form
        """
        uidb64, token, password = get_fields(request.data, ['uid', 'token', 'password'])
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except(TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'message':'Senha alterada com sucesso'})
        return Response({'message':'Token ou uid inválido'}, status=status.HTTP_400_BAD_REQUEST)

    

