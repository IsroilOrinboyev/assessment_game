from django import forms
from .models import Group, Person, Assessment, Question

# ----------------------
# Group creation form
# ----------------------
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-pill text-center shadow-sm animate-glow',
                'placeholder': 'Ex: Party Squad 🎉'
            }),
        }

# ----------------------
# Member add form
# ----------------------
class PersonForm(forms.ModelForm):
    """
    Form to add a new member to a group.
    """
    class Meta:
        model = Person
        fields = ['nickname']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-control rounded-pill text-center shadow-sm animate-glow',
                'placeholder': 'Nickname 🤝'
            }),
        }

# ----------------------
# Assessment score form
# ----------------------
class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control text-center rounded-pill shadow-sm',
                'min': 1,
                'max': 10
            })
        }

# ----------------------
# Question creation form (NEW!)
# ----------------------
class QuestionForm(forms.ModelForm):
    """
    Form to allow creating custom questions before starting assessment.
    """
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control rounded-pill text-center shadow-sm animate-glow',
                'placeholder': 'Write your new question here ✨'
            }),
        }
        labels = {
            'text': 'Question Text'
        }
