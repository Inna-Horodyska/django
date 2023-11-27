from django import forms


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=100)

class TeamForm(forms.Form):
    name = forms.CharField(max_length=100)
    role = forms.CharField(max_length=100)

class TaskForm(forms.Form):
    name = forms.CharField(max_length=100)
    #assignee = forms.ChoiceField(choices=[])
    assignee = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-decription'}))
    # def __init__(self, *args, **kwargs):
    #
    #     #custom_choices = kwargs.pop('custom_choices', None)
    #     nam = kwargs.pop('name', None)
    #     assigne = kwargs.pop('custom_choices', None)
    #     descriptio = kwargs.pop('description', None)
    #     super(TaskForm, self).__init__(*args, **kwargs)
    #
    #
    #     if assigne:
    #         self.fields['assignee'] = assigne
    #         self.fields['name'] = nam
    #         # self.assignee = assignee
    #         self.fields['description'] = descriptio
    #     #     self.assignee['my_field'] = forms.ChoiceField(choices=custom_choices)
    # #
    # #     name = forms.CharField(max_length=100)
    # #     assignee = forms.ChoiceField(choices=[])
    # #     description = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-decription'}))



class EmployeeForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    position = forms.CharField(max_length=100)
    efficiency = forms.CharField(max_length=100)
