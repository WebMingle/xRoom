from django import forms

class CreateRoomForm(forms.Form):
    max_users = forms.IntegerField(min_value=2, max_value=20)
    password = forms.CharField(max_length=20)

class JoinRoomForm(forms.Form):
    room_id = forms.CharField(max_length=25)
    password = forms.CharField(max_length=20)

