from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','password1','password2','email']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants','host']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [ 'avatar','username','email', 'name','bio']