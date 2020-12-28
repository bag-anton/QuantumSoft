from django.urls import path

from tree.views import CachedTreeView
from tree.views import DBTreeView
from tree.views import ResetView

urlpatterns = [
    path("db", DBTreeView.as_view(), name='db'),
    path("cache", CachedTreeView.as_view(), name='cache'),
    path("reset", ResetView.as_view(), name='reset'),
]
