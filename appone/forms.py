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

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['medtipo','juegocompania','fk_plataforma']
        widgets = {
            'medtipo' : forms.Select(attrs={'class':'form-control','placeholder':'Tipo de Juego'}),
            'juegocompania' : forms.TextInput(attrs={'class':'form-control','placeholder':'Comapañia desarrolladora del juego'}),
            'fk_plataforma' : forms.Select(attrs={'class':'form-control','placeholder':'Plataforma del juego'}),
        } 
        
class OrganizacionForm(forms.ModelForm):
    class Meta:
        model = Organizacion
        fields = ['org_nombre','eslogan','tipo_organizacion','comic_primer_vez','objetivo_principal','lugar_creacion']
        widgets = {
            'org_nombre' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la organizacion'}),
            'eslogan' : forms.TextInput(attrs={'class':'form-control','placeholder':'Eslogan de la organizacion'}),
            'tipo_organizacion' : forms.Select(attrs={'class':'form-control','placeholder':'Tipo de Organizacion'}),
            'comic_primer_vez' : forms.TextInput(attrs={'class':'form-control','placeholder':'Primera aparicion en comics de la organizacion'}),
            'objetivo_principal' : forms.Textarea(attrs={'class':'form-control','placeholder':'Objetivo principal de la organizacion'}),
            'lugar_creacion' : forms.TextInput(attrs={'class':'form-control','placeholder':'Lugar de creacion de la organizacion'}),
        } 

class SedeForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = ['sede_nombre','sede_ubicacion','tipo_edificacion','org']
        widgets = {
            'sede_nombre' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la sede'}),
            'sede_ubicacion' : forms.TextInput(attrs={'class':'form-control','placeholder':'Ubicación de la sede'}),
            'tipo_edificacion' : forms.Select(attrs={'class':'form-control','placeholder':'Tipo de edificacion de la sede'}),
            'org' : forms.Select(attrs={'class':'form-control','placeholder':'Organización dueña de la sede'}),
        } 

class PoderForm(forms.ModelForm):
    class Meta:
        model = Poder
        fields = ['ponombre','podescripcion','ponaturaleza']
        widgets = {
            'ponombre' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del Poder'}),
            'podescripcion' : forms.Textarea(attrs={'class':'form-control','placeholder':'Descripción del Poder'}),
            'ponaturaleza' : forms.TextInput(attrs={'class':'form-control','placeholder':'Naturaleza del Poder'}),
        } 

class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        fields = ['objnombre','objmaterial','objdescripcion','objtipo']
        widgets = {
            'objnombre' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del Objeto'}),
            'objmaterial' : forms.TextInput(attrs={'class':'form-control','placeholder':'Material del Objeto'}),
            'objdescripcion' : forms.Textarea(attrs={'class':'form-control','placeholder':'Descripción del Objeto'}),
            'objtipo' : forms.Select(attrs={'class':'form-control','placeholder':'Tipo del Objeto'}),
        } 

class CalMedioForm(forms.ModelForm):
    class Meta:
        model = PerfilMedio
        fields = ['calificacion']
        widgets = {
            'calificacion' : forms.Select(attrs={'class':'form-control','placeholder':'Calificacion del medio del perfil'}),
        } 

class CombateForm(forms.ModelForm):
    class Meta:
        model = Combate
        fields = ['cmblugar']
        widgets = {
            'cmblugar' : forms.TextInput(attrs={'class':'form-control','placeholder':'Lugar del combate'}),
        } 

class CmbRegForm(forms.ModelForm):
    class Meta:
        model = RegistroCombates
        fields = ['fk_obj_reg','id_pers_reg','id_pod_reg','cmbfecha']
        widgets = {
            'fk_obj_reg' : forms.Select(attrs={'class':'form-control','placeholder':'Objeto'}),
            'id_pers_reg' : forms.Select(attrs={'class':'form-control','placeholder':'Personaje'}),
            'id_pod_reg' : forms.Select(attrs={'class':'form-control','placeholder':'Poder'}),
            'cmbfecha' : forms.DateInput(attrs={'class':'date','label':'Fecha del combate','type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}),
        } 