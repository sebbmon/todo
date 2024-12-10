from django.shortcuts import render, redirect
from django.db.models import Case, When
from todo.models import Task

def home(request):
    tasks = Task.objects.filter(is_completed=False)#.order_by('-updated_at')
    
    completed_tasks = Task.objects.filter(is_completed=True)

    if request.method == 'POST':
        sort = request.POST.get('sort', 'created')
        request.session['sort'] = sort
        return redirect('home')

    sort = request.session.get('sort', 'created')

    if sort == 'priority':
        priority_order = Case(
            When(priority='high', then=1),
            When(priority='medium', then=2),
            When(priority='low', then=3),
        )
        tasks = Task.objects.filter(is_completed=False).order_by(priority_order)
        completed_tasks = Task.objects.filter(is_completed=True).order_by(priority_order)
    elif sort == 'alphabetical':
        tasks = Task.objects.filter(is_completed=False).order_by('task')
        completed_tasks = Task.objects.filter(is_completed=True).order_by('task')
    else:
        tasks = Task.objects.filter(is_completed=False).order_by('created_at')
        completed_tasks = Task.objects.filter(is_completed=True).order_by('created_at')

    context = {
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'sort': sort,
    }
    return render(request, 'home.html', context)