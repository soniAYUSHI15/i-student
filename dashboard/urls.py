from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home, name='home'),
    path('notes',views.notes, name='notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete'),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name='notes-details'),

    path('homework', views.homework, name='homework'),
    path('update_homework/<int:pk>', views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete-homework'),

    path('youtube', views.youtube, name='youtube'),

    path('todo', views.todo, name='todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update-todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete-todo'),

    path('books', views.books, name='books'),
]