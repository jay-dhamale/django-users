import threading

import requests
from django.conf import settings
from django.dispatch import Signal, receiver
from django_rest_passwordreset.signals import post_password_reset, reset_password_token_created
from users.utils import (
    reset_password_message, update_password_message, register_message, admin_reset_password_message,
    admin_update_password_message
)

__all__ = [
    'send_registration_email',
    'admin_reset_password_token_created',
    'admin_post_password_reset',
]

"""
Signal arguments: instance
"""
send_registration_email = Signal()
admin_reset_password_token_created = Signal()
admin_post_password_reset = Signal()


class EmailRegistrationThread(threading.Thread):

    def __init__(self, sender, instance, *args, **kwargs):
        self.sender = sender
        self.instance = instance
        threading.Thread.__init__(self)

    def run(self) -> None:
        url = "https://be5706auu0.execute-api.ap-south-1.amazonaws.com/dev/send-email"
        payload = {
            'receiver': self.instance.request.data["email"],
            'subject': 'Email Registration',
            "message": register_message(),
            'email': settings.EMAIL,
            'password': settings.PASSWORD,
        }
        headers = {}
        _ = requests.request("POST", url, headers=headers, data=payload)
        return super().run()


@receiver(send_registration_email)
def send_registration_email_created(sender, instance, *args, **kwargs):
    EmailRegistrationThread(sender=sender, instance=instance).start()


class RestPasswordEmailThread(threading.Thread):

    def __init__(self, sender, instance, reset_password_token, *args, **kwargs):
        self.sender = sender
        self.instance = instance
        self.reset_password_token = reset_password_token
        threading.Thread.__init__(self)

    def run(self) -> None:
        url = "https://be5706auu0.execute-api.ap-south-1.amazonaws.com/dev/send-email"
        payload = {
            'receiver': self.reset_password_token.user.email,
            'subject': 'Reset Password',
            # 'message': f'Testing Email {self.reset_password_token.key}',
            'message': reset_password_message(self.reset_password_token.key),
            'email': settings.EMAIL,
            'password': settings.PASSWORD,
        }
        headers = {}
        _ = requests.request("POST", url, headers=headers, data=payload)
        return super().run()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    RestPasswordEmailThread(sender=sender, instance=instance, reset_password_token=reset_password_token).start()


class UpdatePasswordThreading(threading.Thread):
    def __init__(self, sender, user, *args, **kwargs):
        self.sender = sender
        self.user = user
        threading.Thread.__init__(self)

    def run(self) -> None:
        url = "https://be5706auu0.execute-api.ap-south-1.amazonaws.com/dev/send-email"
        payload = {
            'receiver': self.user.email,
            'subject': 'Update Password',
            'message': update_password_message(),
            'email': settings.EMAIL,
            'password': settings.PASSWORD,
        }
        headers = {}
        _ = requests.request("POST", url, headers=headers, data=payload)
        # print(response.status_code, flush=True)
        return super().run()


@receiver(post_password_reset)
def reset_password(sender, user, *args, **kwargs):
    UpdatePasswordThreading(sender=sender, user=user).start()


# Admin Signals

class AdminRestPasswordEmailThread(threading.Thread):

    def __init__(self, sender, instance, reset_password_token, *args, **kwargs):
        self.sender = sender
        self.instance = instance
        self.reset_password_token = reset_password_token
        threading.Thread.__init__(self)

    def run(self) -> None:
        url = "https://be5706auu0.execute-api.ap-south-1.amazonaws.com/dev/send-email"
        payload = {
            'receiver': self.reset_password_token.user.email,
            'subject': 'Reset Password',
            # 'message': f'Testing Email {self.reset_password_token.key}',
            'message': admin_reset_password_message(self.reset_password_token.key),
            'email': settings.EMAIL,
            'password': settings.PASSWORD,
        }
        headers = {}
        _ = requests.request("POST", url, headers=headers, data=payload)
        return super().run()


@receiver(admin_reset_password_token_created)
def admin_password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    AdminRestPasswordEmailThread(sender=sender, instance=instance, reset_password_token=reset_password_token).start()


class AdminUpdatePasswordThreading(threading.Thread):
    def __init__(self, sender, user, *args, **kwargs):
        self.sender = sender
        self.user = user
        threading.Thread.__init__(self)

    def run(self) -> None:
        url = "https://be5706auu0.execute-api.ap-south-1.amazonaws.com/dev/send-email"
        payload = {
            'receiver': self.user.email,
            'subject': 'Update Password',
            'message': admin_update_password_message(),
            'email': settings.EMAIL,
            'password': settings.PASSWORD,
        }
        headers = {}
        _ = requests.request("POST", url, headers=headers, data=payload)
        # print(response.status_code, flush=True)
        return super().run()


@receiver(admin_post_password_reset)
def admin_reset_password(sender, user, *args, **kwargs):
    AdminUpdatePasswordThreading(sender=sender, user=user).start()
