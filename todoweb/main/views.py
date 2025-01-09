from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import ToDoList, Item
from itertools import chain
from rest_framework import status
from datetime import timedelta
from django.shortcuts import get_object_or_404
from .forms import AddNewTask
from .api.serializers import ToDoListSerializer, ItemSerializer
import json
# Create your views here.


def index(response, id):
    ls = ToDoList.objects.get(id=id)
    incomplete_items = ls.item_set.filter(complete=False)
    complete_items = ls.item_set.filter(complete=True)
    all_items = chain(incomplete_items, complete_items)
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()
    return render(response, "main/list.html", {"ls":ls, "ls_items":all_items})

def home(response):
    return render(response, "main/home.html")
@api_view(['GET', 'POST'])

def create(request):
    if request.method == "POST":
        task = request.data.get("task")
        complete = request.data.get("complete", False)
        duration = request.data.get("duration")

        if not task or not duration:
            return Response(
                {"error": "Task and duration are required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convert duration string to timedelta
        try:
            hours, minutes, seconds = map(int, duration.split(":"))
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            return Response(
                {"error": "Invalid duration format. Expected HH:MM:SS."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            todo_list = ToDoList.objects.get(id=1)
            t = Item(todolist=todo_list, text=task, complete=complete, duration=duration)
            t.save()

            serializer = ItemSerializer(t)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    elif request.method == "GET":
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def one_item(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        item.delete()
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'PUT'])
def todo_items(request):
    try:
        # Fetch the ToDoList with ID 1
        ls = ToDoList.objects.get(id=1)
    except ToDoList.DoesNotExist:
        return Response({"error": "List not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Fetch incomplete items first, then complete items
        incomplete_items = ls.item_set.filter(complete=False)
        complete_items = ls.item_set.filter(complete=True)
        # Combine the querysets (order preserved: incomplete first)
        items = incomplete_items | complete_items
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        # Ensure the request data is a list
        if not isinstance(request.data, list):
            return Response({"error": "Invalid data format, expected a list."}, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        updated_items = []

        for item_data in request.data:
            try:
                # Fetch and update each item
                item = Item.objects.get(id=item_data["id"])
                item.complete = item_data["complete"]
                item.save()
                updated_items.append(item)
            except ObjectDoesNotExist:
                errors.append({"id": item_data["id"], "error": "Item not found."})
            except KeyError as e:
                errors.append({"id": item_data.get("id", None), "error": f"Missing field: {str(e)}."})

        # If there are errors, return a multi-status response
        if errors:
            return Response(
                {
                    "message": "Partial update completed with errors.",
                    "errors": errors,
                },
                status=status.HTTP_207_MULTI_STATUS,
            )

        # Serialize and return all updated items
        serializer = ItemSerializer(updated_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)