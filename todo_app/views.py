from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from .forms import TodoForms
from .models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView


class TaskListView(ListView):
    model = Task
    template_name ='task_view.html'
    context_object_name = 'obj1'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_view.html'
    context_object_name = 'i'



class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
           return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

def task_view(request):
    obj1=Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        priority = request.POST.get('priority')
        date=request.POST.get('date')
        obj = Task(name=name, priority=priority,date=date)
        obj.save()

    return render(request,'task_view.html',{'obj1':obj1})

class TaskDeleteView(DeleteView):
        model = Task
        template_name ='delete.html'
        success_url = reverse_lazy('cbvtask')

def delete(request,taskid):
    if request.method == 'POST':
        task=Task.objects.get(id=taskid)
        task.delete()
        return redirect('/')
    return render(request,'delete.html',{'task_id':taskid})

def update(request,taskid):
   task=Task.objects.get(id=taskid)
   form=TodoForms(request.POST or None,request.FILES,instance=task)
   if form.is_valid():
      form.save()
      return redirect('/')
   return render(request,"edit.html",{'task':task,'form':form})


