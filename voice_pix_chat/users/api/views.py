import random
import time

from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from voice_pix_chat.users.models import User

from .serializers import UserSerializer

User = get_user_model()


class Base:
    mail_verify_code_list = []


def send_mail_verify_code(email, random_num):
    # sending a verification code to mail
    class A:
        status_code = 200

    return A

    email_params = {
        "apikey": "14AA590CAA2F38AD5223327ED4B742748464322A8DF1817600D518DA104A1D56170C042D98928AD687B03B683F35E6E8",
        "from": "sg.pythondev@gmail.com",
        "to": email,
        "subject": "Email Verify - Parakeet Account",
        "body": f"{random_num}",
        "isTransactional": True,
    }

    response = requests.post(
        "https://api.elasticemail.com/v2/email/send",
        data=email_params,
    )
    return response


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.mail_verify:
                # success log in
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "status": {
                            "type": "success",
                            "message": "Welcome back! You have successfully logged in.",
                        },
                        "result": {
                            "token": token.key,
                        },
                        "navigate": "/home",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # User exists but is not mail verified
                random_num = random.randint(100000, 999999)
                print(random_num)
                response = send_mail_verify_code(email, random_num)
                if response.status_code == 200:
                    # not mail verified - pending user
                    Base.mail_verify_code_list.append({"mail": email, "code": random_num, "time": time.time()})
                    return Response(
                        {
                            "status": {
                                "type": "error",
                                "message": "Your email is not verified. We have sent a verification code to your email.",
                            },
                            "result": None,
                            "navigate": "/mail-verify",
                        },
                        status=400,
                    )
                return Response(
                    {
                        "status": {"type": "error", "message": "Sorry, an internal server error occurred."},
                        "navigate": "reload",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            try:
                # User exists but password is not correct
                user = User.objects.get(email=email)
                return Response(
                    {
                        "status": {
                            "type": "error",
                            "message": "Password is not correct.",
                        },
                        "result": None,
                    },
                    status=400,
                )
            except:  # noqa
                # User with provided email does not exist
                return Response(
                    {
                        "status": {
                            "type": "error",
                            "message": "User does not exist.",
                        },
                        "result": None,
                    },
                    status=400,
                )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Delete the user's token
        Token.objects.filter(user=request.user).delete()

        # Logout the user
        logout(request)

        return Response(
            {
                "status": {
                    "type": "success",
                    "message": "You have been successfully logged out.",
                },
                "navigate": "/login",
            }
        )


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            # Check if user with the provided email already exists
            user = User.objects.get(email=email)
            if not user.mail_verify:
                random_num = random.randint(100000, 999999)
                print(random_num)
                response = send_mail_verify_code(email, random_num)
                if response.status_code == 200:
                    # not mail verified - pending user
                    Base.mail_verify_code_list.append({"mail": email, "code": random_num, "time": time.time()})
                    return Response(
                        {
                            "status": {
                                "type": "error",
                                "message": "You are already registered. We have sent a verification code to your email.",
                            },
                            "navigate": "/mail-verify",
                        }
                    )
                else:
                    return Response(
                        {
                            "status": {"type": "error", "message": "Sorry, an internal server error occurred."},
                            "navigate": "reload",
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            return Response(
                {"status": {"type": "error", "message": "You are already registered."}, "navigate": "/login"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:  # noqa
            try:
                # User with the provided email does not exist, proceed with registration
                user = User.objects.create_user(email=email, password=password)
                random_num = random.randint(100000, 999999)
                print(random_num)
                response = send_mail_verify_code(email, random_num)
                if response.status_code == 200:
                    # not mail verified - pending user
                    Base.mail_verify_code_list.append({"mail": email, "code": random_num, "time": time.time()})
                    return Response(
                        {
                            "status": {
                                "type": "success",
                                "message": "We have sent a verification code to your email.",
                            },
                            "result": None,
                            "navigate": "/mail-verify",
                        },
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {
                            "status": {"type": "error", "message": "Sorry, an internal server error occurred."},
                            "navigate": "reload",
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            except:  # noqa
                return Response(
                    {
                        "status": {"type": "error", "message": "Sorry, an internal server error occurred."},
                        "navigate": "reload",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


class ReSendMailVerifyCodeView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            if user.mail_verify == True:
                return Response(
                    {
                        "status": {"type": "info", "message": "Your email has already been verified."},
                        "navigate": "/login",
                    }
                )
            else:
                random_num = random.randint(100000, 999999)
                print(random_num)
                response = send_mail_verify_code(email, random_num)
                if response.status_code == 200:
                    Base.mail_verify_code_list.append({"mail": email, "code": random_num, "time": time.time()})
                    return Response(
                        {
                            "status": {
                                "type": "success",
                                "message": "We have sent a verification code to your email.",
                            },
                            "navigate": "/mail-verify",
                            "result": None,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "status": {"type": "error", "message": "Sorry, an internal server error occurred."},
                            "navigate": "reload",
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
        except:
            return Response(
                {
                    "status": {
                        "type": "error",
                        "message": "User not found. Please register before verifying your email.",
                    },
                    "navigate": "/register",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class MailVerify(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            email = request.data.get("email")
            code = request.data.get("code")
            # user = 1
            try:
                user = User.objects.get(email=email)
                if user.mail_verify == True:
                    return Response(
                        {
                            "status": {"type": "info", "message": "Your email has already been verified."},
                            "navigate": "/login",
                        }
                    )
                verify_code_list = Base.mail_verify_code_list
                if email in [x["mail"] for x in verify_code_list]:
                    if int(code) in [x["code"] for x in verify_code_list]:
                        print(user, "###############")
                        user.mail_verify = True
                        user.save()
                        print(user, "###############")
                        return Response(
                            {
                                "status": {"type": "success", "message": "Email verified successfully"},
                                "navigate": "/login",
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"status": {"type": "error", "message": "Incorrect verification code. Please try again."}},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {
                            "status": {
                                "type": "error",
                                "message": "Verification time has exceeded. Please send a new verification code.",
                            },
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except:
                return Response(
                    {
                        "status": {
                            "type": "error",
                            "message": "User not found. Please register before verifying your email.",
                        },
                        "navigate": "/register",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {
                    "status": {"type": "error", "message": "Sorry, an internal server error occurred."},
                    "navigate": "reload",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
