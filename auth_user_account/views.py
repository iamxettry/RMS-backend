from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .serializers import RegisterSerializers,LoginSerializer, SendPasswordResetEmailSerializer,UserPasswordResetSerializer,UserSerializer
from auth_user_account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import permissions
from rest_framework.permissions import AllowAny



#Function to generate the token for the user
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


# views for registration
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format="json"):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"userdata":serializer.data,"message": "User Created Successfully.Now perform Login to get your token"},status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views for login 
class UserLoginView(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user is not None:
                # Create or retrieve a token for the user
                token = get_tokens_for_user(user)
                # Return the token and user data
                return Response({'token': token, 'user_id': user.id, 'email': user.email,"superUser":user.is_superuser}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
# user Pofile view
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        serializer=UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self,request):
    #     serializer=UserSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response({"Profile":serializer.data,"message": "Profile Uploaded Successfully."},status=status.HTTP_201_CREATED, content_type="application/json")

    #     return Response({"error":serializer.errors,"message": "Failed to upload profile."}, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")
# Email send view
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_link = serializer.validated_data.get('reset_link')

        return Response({'reset_link': reset_link, 'message': 'Password reset link generated successfully'},status=status.HTTP_200_OK)
    

# password reset view
class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    print(serializer)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
