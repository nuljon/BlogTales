from builtins import object
from urllib import request

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic.dates import (ArchiveIndexView, DateDetailView,
                                        DayArchiveView, MonthArchiveView,
                                        TodayArchiveView, WeekArchiveView,
                                        YearArchiveView)
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView

from thewall.models import Brick, Brickmaker, WallPage

from .forms import BrickForm, BrickmakerForm


class BrickmakerUpdate(LoginRequiredMixin, UpdateView):
    model = Brickmaker
    fields = '__all__'
    template_name = 'thewall/brickmaker_update.html'

    #def get_context_data(self, request, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['user'] = request.user

    #    return render(request, self.template_name, {'context': context})

    #form = BrickmakerForm()
    #def post(self, request, *args, **kwargs):
    #    if form.is_valid():
    #        brickmaker=form.save()
    #        return HttpResponseRedirect('')

    #    return render(request, self.template_name, {'form': form})


class BrickmakerFormView(FormView):
    model = Brickmaker
    form_class = BrickmakerForm
    #form = BrickmakerForm
    fields = ('user', 'avatar_image', 'bio')
    template_name = 'brickmaker_edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})




class BrickmakerDetail(DetailView):
    model = Brickmaker
    template_name = 'thewall/brickmaker_detail.html'


    def get(self, request, **kwargs):
        if 'pk' in kwargs:
            pk = kwargs['pk']
            model = get_object_or_404(Brickmaker, pk=pk)

        else:
            model = get_object_or_404(Brickmaker, user=request.user)

        return render(request, self.template_name, {'model': model})

    #def get_context_data(self, request, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['user'] = request.user
    #    return render(request, self.template_name, {'context': context})



"""
    the crispy forms tutorial
    https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html
"""


@login_required(login_url='/login/')
def brick_new(request, wall_page):

    if request.method == "POST":
        form = BrickForm(request.POST)
        if form.is_valid():
            brick = form.save(commit=False)
            brick.wall_page = WallPage.objects.get(id=wall_page)
            brick.author = request.user
            brick.date = timezone.now()
            brick.name = '%s-%s-%s' % (brick.date, brick.author, brick.title)
            brick.save()
            return redirect('brick_detail', pk=brick.pk)
    else:
        form = BrickForm()
    return render(request, 'thewall/brick_edit.html', {'form': form})

def brick_detail(request, pk):
    brick = get_object_or_404(Brick, pk=pk)
    return render(request, 'thewall/brick_detail.html', {'brick': brick})


def brick_edit(request, pk):
     brick = get_object_or_404(Brick, pk=pk)
     if request.method == "POST":
        form = BrickForm(request.POST, instance=brick)
        if form.is_valid():
            brick = form.save(commit=False)
            brick.wall_page = brick.wall_page
            brick.author = request.user
            brick.date = timezone.now()
            brick.name = brick.name
            brick.save()
            return redirect('brick_detail', pk=brick.pk)
     else:
        form = BrickForm(instance=brick)
     return render(request, 'thewall/brick_edit.html', {'form': form})

# def parent_wall(request, wall_page):
