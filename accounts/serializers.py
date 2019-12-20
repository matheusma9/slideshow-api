from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        errors = [] 
        if User.objects.filter(username=username).exists():
            errors.append({'username':'Já existe um usuário com esse username'})

        if User.objects.filter(email=email).exists():
            errors.append({'email':'Já existe um usuário com esse email'})
        try:
            validate_password(password)
        except ValidationError as e:
            errors.append({'password':list(e)})
        if errors:
            raise serializers.ValidationError({'errors':errors})
        return User.objects.create_user(username=username, email=email, password=password, **validated_data)


