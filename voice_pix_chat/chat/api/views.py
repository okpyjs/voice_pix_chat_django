from chat.models import TestModel
from django.contrib.auth import authenticate, login
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from voice_pix_chat.users.models import User

from .serializers import TestSerializer


class TestViewSet(ModelViewSet):
    def list(self, request):
        # Implement your logic for the 'list' action
        queryset = TestModel.objects.all()
        serializer = TestSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Implement your logic for the 'retrieve' action
        instance = TestModel.objects.get(pk=pk)
        serializer = TestSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        # Implement your logic for the 'create' action
        serializer = TestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        # Implement your logic for the 'update' action
        instance = TestModel.objects.get(pk=pk)
        serializer = TestSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        # Implement your logic for the 'partial_update' action
        instance = TestModel.objects.get(pk=pk)
        serializer = TestSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        # Implement your logic for the 'destroy' action
        instance = TestModel.objects.get(pk=pk)
        instance.delete()
        return Response(status=204)


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
                    }
                )
            else:
                # User exists but is not mail verified
                return Response(
                    {
                        "status": {
                            "type": "error",
                            "message": "Your email is not verified.",
                        },
                        "result": None,
                    },
                    status=400,
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


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        # Congratulations! You have successfully registered.
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
            return Response({"status": {"type": "error", "message": "You are already registered."}})
        except:
            pass
