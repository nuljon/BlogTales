from .forms import BrickForm
from .models import Brick
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

def brick_new(request):

    if request.method == "POST":
        form = BrickForm(request.POST)
        if form.is_valid():
            brick = form.save(commit=False)
            """ brick.author = request.user """
            brick.date = timezone.now()
            brick.name = '%s-%s-%s' % (brick.date, brick.author, brick.title)
            brick.wall_page = brick.get_wall_pages.first()
            brick.save()
            return redirect('brick_detail', pk=brick.pk)
    else:
        form = BrickForm()
    return render(request, 'thewall/brick_edit.html', {'form': form})


def brick_detail(request, pk):
    brick = get_object_or_404(Brick, pk=pk)
    return render(request, 'thewall/parts/brick.html', {'brick': brick})
