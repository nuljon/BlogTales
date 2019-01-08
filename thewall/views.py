from builtins import object
from django.shortcuts import get_object_or_404
from .forms import BrickForm
from .models import Brick, WallPage
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import CreateView
from .models import Brickmaker
""" from django.views.generic import ListView
from books.models import Book


class BookList(ListView):
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'

 """
class BrickmakerCreateView(CreateView):
    model = Brickmaker
    fields = ('user', 'avatar_image', 'bio')

"""
    the crispy forms tutorial
    https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html
"""


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
