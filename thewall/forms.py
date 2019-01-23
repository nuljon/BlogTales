from django.forms import ModelForm

from thewall.models import Brick, Brickmaker


class BrickForm(ModelForm):
    class Meta:
        model = Brick
        fields = ('title', 'content')

class BrickmakerForm(ModelForm):
    class Meta:
        model = Brickmaker
        fields = ('user', 'avatar_image', 'bio')
        labels = {'user': 'Message Author','avatar_image': 'Avatar', 'bio': 'Biography'}
        help_texts = {'bio': 'a creative space for you to leave an impression of who you are and perhaps how Johnathon signified in your life.'}

