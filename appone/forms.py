from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django_countries.widgets import CountrySelectWidget


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

class VilanoForm(forms.ModelForm):
    class Meta:
        model = Villano
        fields = ['nombre_supervillano','objetivo','archienemigo']
        widgets = {
            'nombre_supervillano' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el nombre de Villano del personaje'}),
            'objetivo' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el objetivo del villano'}),
            'archienemigo' : forms.Select(attrs={'class':'form-control','placeholder':'Archienemigo del villano'}),
        }              


class MedioForm(forms.ModelForm):
    class Meta:
        model = Medio
        fields = ['medfecestreno','medcomcreacion','medcomproduc','medrating','medsinopsis','medionombre']
        widgets = {
            'medfecestreno' : forms.DateInput(attrs={'class':'date','label':'Fecha de estreno','type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}),
            'medcomcreacion' : forms.TextInput(attrs={'class':'form-control','placeholder':'compañia creadora del medio'}),
            'medcomproduc' : forms.TextInput(attrs={'class':'form-control','placeholder':'compañia productora del medio'}),
            'medrating' : forms.Select(attrs={'class':'form-control','placeholder':'Rating del medio'}),
            'medsinopsis' : forms.Textarea(attrs={'class':'form-control','placeholder':'Sipnopsis del medio'}),
            'medionombre' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del medio'}),
        }  

class PeliForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['medtipo','peldirector','pelduracion','pelcosteprod','pelganancias']
        widgets = {
            'medtipo' : forms.Select(attrs={'class':'form-control','placeholder':'Tipo de la pelicula'}),
            'peldirector' : forms.TextInput(attrs={'class':'form-control','placeholder':'Director de la pelicula'}),
            'pelduracion' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Duracion de la pelicula (En minutos)'}),
            'pelcosteprod' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Coste de producción de la pelicula (en M$)'}),
            'pelganancias' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Ganancias de la pelicula (en M$)'}),

        }       

class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['medtipo','sercreador','serepisodios','sercanal']
        widgets = {
            'medtipo' : forms.Select(attrs={'class':'form-control','placeholder':'Tipo de serie'}),
            'sercreador' : forms.TextInput(attrs={'class':'form-control','placeholder':'Creador de la serie'}),
            'serepisodios' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Numero de episodios de la serie'}),
            'sercanal' : forms.TextInput(attrs={'class':'form-control','placeholder':'Canal de transmision de la serie'}),
        }       