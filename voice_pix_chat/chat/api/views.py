from chat.models import TestModel
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

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
