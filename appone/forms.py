from django import forms
from .models import *
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
        fields = ['username','nombreu','apellidou','correou','password','fechanacu','ciudadu','paisu','sexou']
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de usuario'}),
            'nombreu' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre real de usuario'}),
            'apellidou' : forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido de usuario'}),
            'correou' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo electronico'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña del usuario'}),
            'fechanacu' : forms.DateInput(attrs={'class':'date','label':'Fecha de nacimiento','type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}),
            'paisu' : CountrySelectWidget(),
            'ciudadu' : forms.TextInput(attrs={'class':'form-control','placeholder':'Ciudad de usuario'}),    
            'sexou' : forms.Select(attrs={'class':'form-control','placeholder':'Sexo del usuario'}),
        }
        
class TDCForm(forms.ModelForm):
    class Meta:
        model = Tarjetacredito
        fields = ['tdcnumero','tdcfecvencimiento','tdccvv']
        widgets = {
            'tdcnumero' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Escriba el numero de la tarjeta'}),
            'tdcfecvencimiento' : forms.DateInput(attrs={'class':'date','label':'Fecha de vencimiento','type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}),
            'tdccvv' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Escriba el codigo de la tarjeta'}),
        }        


class PersonajeForm(forms.ModelForm):
    class Meta:
        model = Personaje
        fields = ['genc','primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','color_pelo','color_ojos','comic_primer_vez','estadomarital']
        widgets = {
            'genc' : forms.Select(attrs={'class':'form-control','placeholder':'Genero del personaje'}),
            'primer_nombre' : forms.TextInput(attrs={'class':'form-control','placeholder':'Primer nombre del personaje'}),
            'segundo_nombre' : forms.TextInput(attrs={'class':'form-control','placeholder':'Segundo nombre del personaje'}),
            'primer_apellido' : forms.TextInput(attrs={'class':'form-control','placeholder':'Primer apellido de personaje'}),
            'segundo_apellido' : forms.TextInput(attrs={'class':'form-control','placeholder':'Segundo apellido de personaje'}),   
            'color_pelo' : forms.TextInput(attrs={'class':'form-control','placeholder':'Color del pelo del personaje'}),
            'color_ojos' : forms.TextInput(attrs={'class':'form-control','placeholder':'Color de los ojos del personaje'}),
            'comic_primer_vez' : forms.TextInput(attrs={'class':'form-control','placeholder':'Primera aparición en comics del personaje'}),  
            'estadomarital' : forms.Select(attrs={'class':'form-control','placeholder':'Estado Marital del personaje'}),
        }

class HeroeForm(forms.ModelForm):
    class Meta:
        model = Heroe
        fields = ['nombre_superheroe','color_traje','logotipo']
        widgets = {
            'nombre_superheroe' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el nombre de Héroe del personaje'}),
            'color_traje' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el color del traje del héroe'}),
            'logotipo' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el logotipo del personaje del héroe'}),
        }      