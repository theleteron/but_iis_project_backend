from django.urls import path
from .views import LibraryViews

urlpatterns = [
    path('library/', LibraryViews.as_view()),
    path('library/<int:id>', LibraryViews.as_view())
]