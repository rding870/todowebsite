from rest_framework.routers import DefaultRouter
from main.api.urls import todolist_router, item_router
from django.urls import path, include

router = DefaultRouter()
router.registry.extend(todolist_router.registry)
router.registry.extend(item_router.registry)

urlpatterns = [
    path('', include(router.urls))
]