# Standard Imports

# 3rd party libraries imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

# app imports
from users.models import Users, UsersDevices
from users.serializers import UsersSerializer, UsersDevicesSerializer, RegisterSerializer, ResendOTPSerializer, VerifyAccountSerializer, UploadIDSerializer
from users.filters import UsersFilter, UsersDevicesFilter
from users.signals import send_registration_email
from atomicloops.viewsets import AtomicViewSet
from atomicloops.permissions import UsersPermission
from users.serializers import UpdateAdminStatusSerializer
from utils.aws_script import upload_image
from users.utils import send_otp, resend_otp
import random
from firebase_admin import auth
from utils.email import send_email
from django.conf import settings


# Users View
class UsersView(AtomicViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, UsersPermission]
    filterset_class = UsersFilter
    search_fields = [
        'firstName',
        'lastName',
        'email',
    ]
    ordering_fields = (
        'createdAt',
        'updatedAt',
    )

    # This will be used as the default ordering
    ordering = ('-createdAt',)

    def create(self, request, *args, **kwargs):
        return Response("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['post'], url_path='multiple-create')
    def multiple_create(self, request, *args, **kwargs):
        return Response("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['post'], url_path='upload-id')
    def upload_id(self, request, *args, **kwargs):
        image = request.FILES.get('file', None)
        if not image:
            return Response("Image not found", status=status.HTTP_400_BAD_REQUEST)
        governmentIdURL = upload_image(image, folder="ID-Proofs")
        data = {
            'governmentIdURL': governmentIdURL
        }
        serialized_data = UploadIDSerializer(instance=request.user, data=data, partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='update-admin-user')
    def update_admin_user(self, request, *args, **kwargs):
        try:
            serializer_class = UpdateAdminStatusSerializer
            if not request.user.is_superuser:
                return Response("Unauthorized user", status=status.HTTP_403_FORBIDDEN)
            if not isinstance(request.data, list):
                raise ValidationError('Request body must be a list')
            if request.data == []:
                raise ValidationError('Empty data not permitted')
            if len(request.data) > 100:
                raise ValidationError('Number of list elements must not be greater than 100')
            ids = self.validate_ids(request.data)
            instances = Users.objects.filter(id__in=ids)
            fields = [f.name for f in Users._meta.concrete_fields]
            fields.remove('id')
            _ = Users.objects.bulk_update(instances, fields)
            serializer = serializer_class(instances, many=True, partial=True, context={'request': self.request, 'view': self})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        tokens = OutstandingToken.objects.filter(user_id=instance.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Register Users
class RegisterUserView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        userInput = request.data
        userInput['otp'] = str(random.randint(100000, 999999))
        userInput["signInMethod"] = "email"
        print("SENDING: ", userInput, flush=True)
        serializer = RegisterSerializer(data=userInput)

        if serializer.is_valid():
            serializer.save()  # user is saved in db
            # message = 'Your otp for al classifier is: ' + str(userInput['otp'])
            message = send_otp(str(userInput['otp']))
            send_email(settings.EMAIL, settings.PASSWORD, userInput['email'], 'verification otp', message)
            return Response("ok", status.HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status.HTTP_400_BAD_REQUEST)


# users devices views
class UsersDevicesView(ModelViewSet):
    queryset = UsersDevices.objects.all()
    serializer_class = UsersDevicesSerializer
    filterset_class = UsersDevicesFilter
    search_fields = [
        'userId__firstName',
        'userId__lastName',
        'userId__email',
    ]
    ordering_fields = (
        'createdAt',
        'updatedAt',
    )

    # This will be used as the default ordering
    ordering = ('-createdAt',)

    def create(self, request, *args, **kwargs):
        request.data['userId'] = request.user.id
        # print(request.data, flush=True)
        return super().create(request, *args, **kwargs)


# Upload Image API
class UploadImageView(APIView):
    serializer_class = UsersSerializer

    def post(self, request, *args, **kwargs):
        file = request.FILES['file'] if 'file' in request.FILES else None

        if file is None:
            return Response({"message": "File Not Provided"}, status.HTTP_400_BAD_REQUEST)

        url = upload_image(file, folder="profiles")
        if url is None:
            return Response({"message": "File not Uploaded"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "OK", "imageUrl": url}, status.HTTP_201_CREATED)


class VerifyAccountView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            data = request.data
            email = data['email']
            user = Users.objects.filter(email=email).first()
            serializer = VerifyAccountSerializer(data=data, instance=user)
            if serializer.is_valid():
                user = serializer.save()
                send_registration_email.send(sender=self.__class__, instance=self)
                token = RefreshToken.for_user(user)
                data = {
                    'refresh': str(token),
                    'access': str(token.access_token),
                }
                return Response(data, status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"internal server error {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR, )


# Register Google User
class RegisterGoogleUserView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            token = data.get('token')
            fb_data = auth.verify_id_token(token)
            data = {
                "firstName": fb_data.get('name'),
                "email": fb_data.get('email'),
                "profilePicture": fb_data.get('picture'),
                "signInMethod": "google",
            }
            request.data["email"] = fb_data.get('email')
            print("SENDING: ", data, flush=True)
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                token = RefreshToken.for_user(user)
                data = {
                    'refresh': str(token),
                    'access': str(token.access_token),
                    'message': 'User Registered Successfully With Google'
                }
                send_registration_email.send(sender=self.__class__, instance=self)
                # print("PAYLOAD" , flush=True)
                # print(settings.EMAIL,settings.PASSWORD,user.email , flush=True)
                # send_mail_thread(email=settings.EMAIL,
                #                 password=settings.PASSWORD,
                #                 receiver=user.email,
                #                 subject="Email Registration With Google",
                #                 message=register_message(),
                #                 cc="")
                return Response(
                    data, status.HTTP_201_CREATED
                )
            return Response({"message": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

# users devices views


class ResendOTPView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            userInput = request.data
            userInput['otp'] = str(random.randint(100000, 999999))
            user = Users.objects.filter(email=userInput["email"]).first()
            serializer = ResendOTPSerializer(data=userInput, instance=user)
            if serializer.is_valid():
                user = serializer.save()  # user is saved in db
                message = resend_otp(str(userInput['otp']))
                send_email(settings.EMAIL, settings.PASSWORD, userInput['email'], 'verification otp', message)
                return Response("OK", status.HTTP_201_CREATED)
            return Response({"message": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
