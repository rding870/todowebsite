from django import forms

class AddNewTask(forms.Form):
    task = forms.CharField(label="Task", max_length = 200)
    complete = forms.BooleanField(required=False)
    duration = forms.DurationField()