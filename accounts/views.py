from builtins import object
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify

from .forms import CreateNewFrontendUser


""" from django.views.generic import ListView
from books.models import Book


class BookList(ListView):
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'

 """

"""
    the crispy forms tutorial
    https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html
"""


def home(request):
    return redirect('/')


def signup(request):
    if request.method == 'POST':
        form = CreateNewFrontendUser(request.POST)
        if form.is_valid():
            user = form.save()
            pk=user.id
            return redirect('BrickmakerUpdate', pk)

    else:
        form = CreateNewFrontendUser()
    return render(request, 'registration/signup.html', {'form': form})




@login_required
def secret_page(request):
    return render(request, 'secret_page.html')


class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'secret_page.html'
