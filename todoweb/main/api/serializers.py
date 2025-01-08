from rest_framework.serializers import ModelSerializer
from ..models import ToDoList, Item

class ToDoListSerializer(ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ('id', 'name')
class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'todolist', 'text', 'complete', 'duration')