from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import ToDoList, Item
from itertools import chain
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

def create(response):
    if response.method == "POST":
        form = AddNewTask(response.POST) # Dictionary of all the different attributes
        if form.is_valid():
            task = form.cleaned_data["task"]
            complete = form.cleaned_data["complete"]
            duration = form.cleaned_data["duration"]
            t = Item(todolist=ToDoList.objects.get(id=1), text=task, complete=complete, duration=duration)
            t.save()
        return HttpResponseRedirect("/1")
    else:
        form = AddNewTask()
    return render(response, "main/create.html", {"form":form})

@api_view(['GET', 'POST'])
def todo_list_detail(request, id):
    try:
        ls = ToDoList.objects.get(id=id)
    except ToDoList.DoesNotExist:
        return Response({"error": "List not found"}, status=404)

    if request.method == 'GET':
        serializer = ToDoListSerializer(ls)
        return Response(serializer.data)

    if request.method == 'POST':
        task = request.data.get("task")
        if task:
            new_item = Item(todolist=ls, text=task, complete=False)
            new_item.save()
            return Response({"message": "Task saved successfully!"}, status=201)
@api_view(['GET', 'PUT'])
def todo_items(request, id):
    try:
        ls = ToDoList.objects.get(id=id)
    except ToDoList.DoesNotExist:
        return Response({"error": "List not found"}, status=404)

    if request.method == 'GET':
        incomplete_items = ls.item_set.filter(complete=False)
        complete_items = ls.item_set.filter(complete=True)
        items = incomplete_items.union(complete_items, all=True)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        if not isinstance(request.data, list):
            return Response({"error": "Invalid data format, expected a list."}, status=400)

        errors = []
        for item_data in request.data:
            try:
                item = Item.objects.get(id=item_data["id"])
                item.complete = item_data["complete"]
                item.save()
            except ObjectDoesNotExist:
                errors.append({"id": item_data["id"], "error": "Item not found."})
            except KeyError:
                errors.append({"id": item_data.get("id", None), "error": "Missing fields."})

        if errors:
            return Response({"message": "Partial update completed with errors.", "errors": errors}, status=207)

        return Response({"message": "Items updated successfully!"})