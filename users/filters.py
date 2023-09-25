from atomicloops.filters import AtomicFilter
from .models import Users, UsersDevices


class UsersFilter(AtomicFilter):
    class Meta:
        model = Users
        fields = (
            'createdAt',
            'updatedAt',
            'is_active',
            'is_superuser',
            'is_staff',
            'level'
        )


class UsersDevicesFilter(AtomicFilter):
    class Meta:
        model = UsersDevices
        fields = (
            'createdAt',
            'updatedAt',
            'userId',
        )
