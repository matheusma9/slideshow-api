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

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all() 
    permission_classes = [IsOwnerOrCreateOnly]

    @action(methods=['post'], detail=False)
    def solicitar(self, request):
        domain = request.data['domain']
        to_email = request.data.get('email')
        user = get_object_or_404(User, email=to_email)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('accounts/pass_reset.html', {
            'user': user,
            'domain': domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return Response('A solicitação será enviada para o seu email.')
    
    @action(methods=['post'], detail=False)
    def reset(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response('Senha alterada com sucesso')
        return Response('Token ou uid inválido', status=status.HTTP_400_BAD_REQUEST)

    

