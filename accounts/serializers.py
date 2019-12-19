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
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Esse username já existe')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Esse email já existe')    
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'error':list(e)})
        return User.objects.create_user(username=username, email=email, password=password, **validated_data)
