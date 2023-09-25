from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Homework,Todo
from .forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
from django.contrib.auth.decorators import login_required
# Create your views here.

def Home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title = request.POST['title'], description = request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully")

    else:
        form = NotesForm()
    notes = Notes.objects.filter(user = request.user)
    context = {'notes':notes,'form':form}
    return render(request, 'dashboard/notes.html',context)

@login_required
def delete_note(request, pk= None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request, f'Homework Added from {request.user.username}!')

    else:
        form = HomeworkForm

    homework = Homework.objects.filter(user = request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
                'homeworks':homework, 
                'homeworks_done': homework_done,
                'form':form,
    }
    return render(request, 'dashboard/homework.html',context)

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

@login_required
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results' : result_list,
            }
        return render(request, "dashboard/youtube.html", context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/youtube.html', context)

@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"Todo Added from {request.user.username}!")
    else:
        form = TodoForm
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else: 
        todos_done = False
    context = {
        'todos': todo,
        'form' : form,
        'todos_done' : todos_done
    }
    return render(request, "dashboard/todo.html",context)

@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

@login_required
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                'subtitle' : answer['items'][i]['volumeInfo'].get('subtitle'),
                'description' : answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories' : answer['items'][i]['volumeInfo'].get('categories'),
                'rating' : answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail' : answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview' : answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context={
                'form':form,
                'results' : result_list,
            }
        return render(request, "dashboard/books.html", context)
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/books.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        'form':form,
    }
    return render(request, "dashboard/register.html",context)

def profile(request):
    homeworks = Homework.objects.filter(is_finished = False, user = request.user)
    todos = Todo.objects.filter(is_finished = False, user = request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    
    context = {
        'homeworks' : homeworks,
        'todos' : todos,
        'homework_done' : homework_done,
        'todos_done' : todos_done,
    }
    return render(request, "dashboard/profile.html", context)