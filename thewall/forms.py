from django.forms import ModelForm

from thewall.models import Brick


class BrickForm(ModelForm):
    class Meta:
        model = Brick
        fields = ('title', 'content', 'author')

