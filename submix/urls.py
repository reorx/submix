from django.contrib import admin
from django.urls import path

from .views import IndexView, NodesView, APINodesView


urlpatterns = [
    path('', IndexView.as_view()),
    path('nodes', NodesView.as_view()),
    path('api/nodes', APINodesView.as_view()),
    path('admin/', admin.site.urls),
]
