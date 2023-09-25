from rest_framework import serializers
from atomicloops.serializers import AtomicSerializer
from .models import Users, UsersDevices, ExportData
from django.contrib.auth.password_validation import validate_password


class UsersSerializer(AtomicSerializer):
    # TODO
    # def validate(self, attrs):
    #     return super().validate(attrs)

    class Meta:
        model = Users
        read_only_fields = ('email', 'is_superuser')
        fields = (
            'id',
            'createdAt',
            'updatedAt',
            'firstName',
            'lastName',
            'email',
            'level',
            'is_active',
            'is_staff',
            'is_superuser',
            'profilePicture',
        )
        get_fields = (
            'id',
            'createdAt',
            'updatedAt',
            'firstName',
            'lastName',
            'email',
            'level',
            'is_active',
            'is_staff',
            'is_superuser',
            'profilePicture',
        )
        list_fields = (
            'id',
            'createdAt',
            'updatedAt',
            'firstName',
            'lastName',
            'email',
            'level',
            'is_active',
            'is_staff',
            'is_superuser',
            'profilePicture',
        )

    def create(self, validated_data):
        # print("I am authenticated", validated_data, flush=True)
        user = Users.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UsersDevicesSerializer(AtomicSerializer):
    class Meta:
        model = UsersDevices
        fields = (
            'id',
            'createdAt',
            'updatedAt',
            'userId',
            'deviceId',
            'token',
            'deviceType',
        )
        get_fields = fields
        list_fields = fields


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = (
            'id',
            'createdAt',
            'updatedAt',
            'firstName',
            'lastName',
            'email',
            'password',
            'level',
            "password",
            'is_active',
            'is_staff',
            'is_superuser',
            'profilePicture',
            'signInMethod',
            'otp',
        )

    # def update(self, instance, validated_data):
    #     print("UPDATE:" , validated_data, flush=True)
    #     if validated_data["signInMethod"] == "google":
    #         instance.is_active = True
    #         instance.isVerified = True
    #         instance.save()
    #     return instance

    def create(self, validated_data):
        # print("I am authenticated", validated_data, flush=True)
        user = Users.objects.create(**validated_data)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
        if validated_data["signInMethod"] == "google":
            user.is_active = True
            user.isVerified = True
        user.save()
        return user

    def validate(self, data):
        if ((data["signInMethod"] == "email") and ("password" not in data)):
            raise serializers.ValidationError({"Password is required for email registration"})
        return data

    @property
    def errors(self):
        # get errors
        errors = super().errors
        verbose_errors = {}

        # fields = { field.name: field.verbose_name } for each field in model
        fields = {field.name: field.verbose_name for field in
                  self.Meta.model._meta.get_fields() if hasattr(field, 'verbose_name')}

        # iterate over errors and replace error key with verbose name if exists
        for field_name, error in errors.items():
            if field_name in fields:
                verbose_errors[str(fields[field_name])] = error
            else:
                verbose_errors[field_name] = error
        return verbose_errors


class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True, required=True)
    oldPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('oldPassword', 'password', 'confirmPassword')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_oldPassword(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"oldPassword": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()
        return instance


# admin user serialzer
class UpdateAdminStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = (
            'id',
            'is_superuser',
            'level',
        )


class ExportDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExportData
        fields = (
            'id',
            'createdAt',
            'updatedAt',
            'userId',
            'modelName',
            'fileUrl'
        )


class ResendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'email',
            'otp',
        )

    def validate(self, data,):
        user = Users.objects.filter(email=data['email'])
        if not user.exists():
            raise serializers.ValidationError(f"User with email {data['email']} does not exist")
        if (user.first().isVerified):
            raise serializers.ValidationError(f"User with email {data['email']} is already verified")
        return data


class VerifyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'email',
            'otp',
        )

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.isVerified = True
        instance.save()
        return instance

    def validate(self, data,):
        user = Users.objects.filter(email=data['email'])
        if user.first().otp != data["otp"]:
            raise serializers.ValidationError("The otp entered does not match")
        if not user.exists():
            raise serializers.ValidationError(f"User with email {data['email']} does not exist")
        if (user.first().isVerified):
            raise serializers.ValidationError(f"User with email {data['email']} is already verified")
        return data


class UploadIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'governmentIdURL')
