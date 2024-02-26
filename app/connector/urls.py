from django.urls import path

from . import views

urlpatterns = [
    path(
        'login/',
        views.UserLoginView.as_view(),
        name='api_login',
    ),
    path(
        'registration/',
        views.UserRegistrationView.as_view(),
        name='api_register',
    ),
    path(
        'send-otp/',
        views.EmailVerificationViewSet.as_view({'post': 'send_otp'}),
        name='api_verification',
    ),
    path(
        'verify-otp/',
        views.EmailVerificationViewSet.as_view({'post': 'verify_otp'}),
        name='api_verification',
    ),
    path(
        'user/',
        views.UserViewSet.as_view(
            {'get': 'retrieve', 'delete': 'delete', 'put': 'update'}
        ),
        name='user',
    ),
]
