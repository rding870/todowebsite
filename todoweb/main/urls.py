# Define paths to different webpages/views in "main" app
from django.urls import path, include
from . import views
from .views import index
urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path('api/', include('main.api.urls')),
    
    ##path('api/todo-lists/<int:id>/', views.todo_list_detail, name='todo_list_detail'),
    path('api/todo-items/', views.todo_items, name='todo_items'),
    path('api/todo-items/<int:id>/', views.one_item, name='one_item'),
]

