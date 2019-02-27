from django.forms import ModelForm, HiddenInput

from thewall.models import Brick, Brickmaker


class BrickForm(ModelForm):
    class Meta:
        model = Brick
        fields = ('title', 'content')

class BrickmakerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(BrickmakerForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = HiddenInput()
    class Meta:
        model = Brickmaker
        fields = ('user', 'avatar_image', 'content')
        labels = {'user': 'Message Author','avatar_image': 'Avatar', 'content': 'Biography'}
        help_texts = {'content': 'a creative space for you to leave an impression of who you are and perhaps how Johnathon signified in your life.'}

