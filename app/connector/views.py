from django.forms import model_to_dict
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from connector.operations import EmailVerificationOperations, UserOperations
from connector.permissions import HasAccessPermissions
from connector.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


@extend_schema(tags=['user login'])
class UserLoginView(APIView):
    """
    User login view
    """

    permission_classes = (permissions.AllowAny,)

    serializer_class = UserLoginSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Request success'),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
        request=serializer_class,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)


@extend_schema(tags=['user register'])
class UserRegistrationView(APIView):
    """
    User registration view
    """

    permission_classes = (permissions.AllowAny,)

    serializer_class = UserRegistrationSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Request success'),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
        request=serializer_class,
    )
    def post(self, request, *args, **kwargs):
        # Other than admin that was required,
        # this endpoint also can create/register users
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['user'])
class UserViewSet(viewsets.ViewSet):
    """
    User view
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, HasAccessPermissions)

    serializer_class = UserSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Request success'),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
        request=serializer_class,
    )
    def update(self, request):
        """
        Updates user information
        """
        username = request.user.username
        user_instance = UserOperations().get_user_instance(username)

        UserOperations().update_user(
            user_data=request.data,
            context={'request': request},
            user_instance=user_instance,
        )

        return Response(
            data='User information updated successfully',
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Request success'),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
        request=serializer_class,
    )
    def retrieve(self, request):
        username = request.user.username
        user_instance = UserOperations().get_user_instance(username)

        return Response(
            model_to_dict(user_instance),
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Request success'),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        }
    )
    def delete(self, request):
        """
        Deletes User on given id
        """
        username = request.user.username

        user_instance = UserOperations().get_user_instance(username)

        UserOperations().delete_user_record(user_instance)

        return Response(
            {f'User  {username} was successfully deleted'},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['email verification'])
class EmailVerificationViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, HasAccessPermissions)

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Request success'),
            400: OpenApiResponse(description='Invalid value'),
            403: OpenApiResponse(description='Permission Denied'),
            500: OpenApiResponse(description='Internal server error'),
        },
    )
    def send_otp(self, request):
        user_id = request.user.id
        email = UserOperations().get_user_instance(user_id).email
        if not email:
            return Response(
                {'error': 'Email not provided'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = EmailVerificationOperations().send_otp_to_email(email)

        # Storing the OTP in session for verification
        request.session['otp'] = otp
        request.session['email'] = email

        response = {'message': f'OTP send to your email {email} successfully'}

        return Response(response, status.HTTP_200_OK)

    def verify_otp(self, request):
        user_id = request.user.id
        user_instance = UserOperations().get_user_instance(user_id)

        submitted_otp = request.data.get('otp')
        stored_otp = request.session.get('otp')

        if not submitted_otp:
            return Response(
                {'error': 'OTP not provided'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if submitted_otp != stored_otp:
            return Response(
                {'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST
            )

        # update user information
        user_information = {'email_verified': True}
        UserOperations().update_user(user_information, user_instance, request)

        return Response({'message': 'Email verification successful'})
