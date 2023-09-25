from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import Response
from rest_framework.permissions import AllowAny
from rest_framework import exceptions, status
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Users
from users.serializers import RegisterSerializer
from rest_framework.views import APIView
from firebase_admin import auth
from users.signals import send_registration_email


# Custom Failure Class
class TokenBackendError(Exception):
    pass


class DetailDictMixin:
    def __init__(self, detail=None, code=None):
        """
        Builds a detail dictionary for the error to give more information to API
        users.
        """
        detail_dict = {"detail": self.default_detail, "code": self.default_code}

        if isinstance(detail, dict):
            detail_dict.update(detail)
        elif detail is not None:
            detail_dict["detail"] = detail

        if code is not None:
            detail_dict["code"] = code

        super().__init__(detail_dict)


class AuthenticationFailed(DetailDictMixin, exceptions.AuthenticationFailed):
    pass


class TokenError(Exception):
    pass


class InvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Token is invalid or expired"
    default_code = "token_not_valid"


# Add more info to Token
class CustomTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, data):
        """
        Check if the user exists.
        """
        # data = s
        _ = super().validate(data)
        user = Users.objects.filter(email=data['email'])
        if not Users.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(f"User with email {data['email']} does not exist")
        if not user.first().is_active:
            raise serializers.ValidationError(f"User with email {data['email']} is inactive")
        token = RefreshToken.for_user(user.first())
        data = dict()
        data['refresh'] = str(token)
        data['access'] = str(token.access_token)
        return data


# Add more info to Token
class AdminCustomTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self, data):
        """
        Check if the user exists.
        """
        _ = super().validate(data)
        user = Users.objects.filter(email=data['email'])
        if not Users.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(f"User with email {data['email']} does not exist")
        if not user.first().is_active:
            raise serializers.ValidationError(f"User with email {data['email']} is inactive")
        if not user.first().is_superuser:
            raise serializers.ValidationError(f"User with email {data['email']} is not admin")
        if not user.first().level == 5:
            raise serializers.ValidationError(f"User with email {data['email']} is not admin")

        token = RefreshToken.for_user(user.first())
        data = dict()
        data['refresh'] = str(token)
        data['access'] = str(token.access_token)
        return data


# Get Token View
class LoginView(APIView):
    """
    Takes email and password as input  and returns an access type JSON web
    token and a refresh type JSON web token
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = CustomTokenPairSerializer

    def get(self, request, *args, **kwargs):
        serializer = CustomTokenPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# Get Token View
class AdminLoginView(TokenObtainPairView):
    """
    Takes email and password as input  and returns an access type JSON web
    token and a refresh type JSON web token.
    This view is only for admin users
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = AdminCustomTokenPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# class RefreshTokenView(TokenRefreshView):
#     # permission_classes = (AllowAny,)
#     # authentication_classes = ()
#     # serializer_class = TokenRefreshSerializer
#     # renderer_classes = [AtomicJsonRenderer]

#     # def post(self, request, *args, **kwargs):
#     #     serializer = self.serializer_class(data=request.data)
#     #     try:
#     #         serializer.is_valid(raise_exception=True)
#     #     except TokenError as e:
#     #         raise InvalidToken(e.args[0])
#     #     # obj =  User.objects.filter(email=request.data['email']).first()
#     #     # serializer.validated_data['email'] = obj.email
#     #     # serializer.validated_data['id'] = obj.id
#     #     # serializer.validated_data['firstName'] = obj.firstName
#     #     return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GoogleLoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            id_token = request.data['token']
            decoded_data = auth.verify_id_token(id_token)
            email = decoded_data.get('email')
            if not email:
                return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            user = Users.objects.filter(email=email).first()
            if user:
                if not user.is_active:
                    raise AuthenticationFailed("User is inactive")
                token = RefreshToken.for_user(user)
                data = dict()
                data['refresh'] = str(token)
                data['access'] = str(token.access_token)
                data['message'] = "User logged in successfully with google"
                return Response(data, status=status.HTTP_200_OK)

            # Create user
            data = {
                "firstName": decoded_data.get('name'),
                "email": decoded_data.get('email'),
                "profilePicture": decoded_data.get('picture'),
                "signInMethod": "google",
            }
            serializer = RegisterSerializer(data=decoded_data)
            if serializer.is_valid():
                user = serializer.save()
                token = RefreshToken.for_user(user)
                data = {
                    'refresh': str(token),
                    'access': str(token.access_token),
                    'message': 'User Registered Successfully With Google'
                }
                request.data["email"] = decoded_data.get('email')
                send_registration_email.send(sender=self.__class__, instance=self)
                return Response(
                    data, status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
