from django import forms
from .models import Task,Usuario
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django_countries.widgets import CountrySelectWidget


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escribe el titulo de la tarea'}),
            'description' : forms.Textarea(attrs={'class':'form-control','placeholder':'Escribe la descripcion de la tarea'}),
            'important' : forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class UsuarioForm(forms.ModelForm):
    
    password2 = forms.CharField(label='confirmacion de contraseña', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese una contraseña de nuevo',
            'id':'password2',
            'required':'required',
        }
    ))
    class Meta:
        model = Usuario
        fields = ['idu','nombreu','apellidou','correou','contrasennau','fechanacu','ciudadu','paisu','sexou']
        widgets = {
            'idu' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de usuario'}),
            'nombreu' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre real de usuario'}),
            'apellidou' : forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido de usuario'}),
            'correou' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo electronico'}),
            'contrasennau' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña del usuario'}),
            'fechanacu' : forms.DateInput(attrs={'class':'date','label':'Fecha de nacimiento','type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}),
            'paisu' : CountrySelectWidget(),
            'ciudadu' : forms.TextInput(attrs={'class':'form-control','placeholder':'Ciudad de usuario'}),    
            'sexou' : forms.Select(attrs={'class':'form-control','placeholder':'Sexo del usuario'}),
        }
        