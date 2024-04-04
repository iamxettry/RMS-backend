from rest_framework import serializers
from .models import accountUser,UserProfile

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core.mail import EmailMessage



# user registration serializer
class RegisterSerializers(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, style={'input_type':'password'})
    class Meta:
        model=accountUser
        fields=['email','username','password']


    def create(self, validated_data):
        return accountUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


# user login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # username=serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})   



# user profie serializer
class UserProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model=UserProfile
      fields=['profile_picture']
#user profile serializer
class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(source='user', read_only=True)
    class Meta:
        model = accountUser
        fields = ['id', 'username', 'email','is_superuser','user_profile']


# mail send serializers

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email=attrs.get('email')
        if accountUser.objects.filter(email=email).exists():
            user = accountUser.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link = f'http://localhost:3000/auth/reset-password/{uid}/{token}'
            # subject='Reset your Password'
            # body = f'Click Following Link to Reset Your Password {link}'
            # email_from='rajuchhetry11@gmail.com'
            # recipient_list = [user.email]
            # try:
            #     send_mail(
            #         subject,
            #         body,
            #         email_from,
            #         [recipient_list],
            #         fail_silently=False,
            #     )
            # except Exception as e:
            #     raise serializers.ValidationError(f'Error sending password reset email: {e}')

            attrs['reset_link'] = link
            return attrs
        else:
            raise serializers.ValidationError("This Email Does not Exist")

# password reset serializers
class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirmPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'confirmPassword']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      confirmPassword = attrs.get('confirmPassword')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != confirmPassword:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = accountUser.objects.get(id=id)
      print(user)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')