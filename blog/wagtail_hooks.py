from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import (Profile)

''' This is stub of what I hope to move into admin on its own, currently Profile class is a snippet and can be configured in that area of admin '''

class ProfileAdmin(ModelAdmin):
    model = Profile
    menu_label = 'User Profiles'  # ditch this to use verbose_name_plural from model
    menu_icon = 'user'
    list_display = ('user','motto','biography', 'githubURL','linkedinURL','background_image')
    search_fields = ('user')
