from rest_framework.viewsets import ModelViewSet
from ..models import ToDoList, Item
from rest_framework.response import Response
from rest_framework import status
from .serializers import ToDoListSerializer, ItemSerializer

class ToDoListViewSet(ModelViewSet):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer

class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
