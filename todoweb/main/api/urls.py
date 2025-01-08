from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToDoListViewSet, ItemViewSet

# Define routers
router = DefaultRouter()
router.register(r'todo-lists', ToDoListViewSet, basename='todo-list')

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include the router's URL patterns
]
