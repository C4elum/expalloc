from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    document = forms.FileField()

    class Meta:
        model = Student
        fields = ['name', 'branch', 'cgpa', 'document']


from django import forms

class SendRequestForm(forms.Form):
    pass
